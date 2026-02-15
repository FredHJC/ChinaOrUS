from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session as DBSession

from database import Base, engine, get_db
from models import Answer, Session
from questions import get_questions_for_frontend
from schemas import ResultResponse, SubmitRequest, SubmitResponse, ChartData
from scoring import calculate_scores
from export import generate_pdf

# 创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="留学生去留决策量表 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/questions")
def get_questions():
    """返回题库（不含分数信息）"""
    return get_questions_for_frontend()


@app.post("/api/submit", response_model=SubmitResponse)
def submit_answers(req: SubmitRequest, db: DBSession = Depends(get_db)):
    """提交答案，计算分数并存储"""
    answers_dicts = [a.model_dump() for a in req.answers]
    result = calculate_scores(req.age, req.age_weight, answers_dicts)

    import uuid
    session_id = str(uuid.uuid4())

    session = Session(
        id=session_id,
        age=req.age,
        us_total_score=result["us_total_score"],
        cn_total_score=result["cn_total_score"],
        quadrant=result["quadrant"],
        diagnosis=result["diagnosis"],
    )
    db.add(session)

    # 存年龄题答案
    db.add(Answer(
        session_id=session_id,
        question_id=0,
        selected_option=str(req.age),
        weight=req.age_weight,
    ))

    # 存选择题答案
    for ans in req.answers:
        db.add(Answer(
            session_id=session_id,
            question_id=ans.question_id,
            selected_option=ans.selected_option,
            weight=ans.weight,
        ))

    db.commit()
    db.refresh(session)

    return SubmitResponse(
        session_id=session.id,
        quadrant=result["quadrant"],
        quadrant_label=result["quadrant_label"],
        diagnosis=result["diagnosis"],
        chart_data=ChartData(
            us_score=result["us_total_score"],
            cn_score=result["cn_total_score"],
            threshold=result["threshold"],
        ),
    )


@app.get("/api/result/{session_id}", response_model=ResultResponse)
def get_result(session_id: str, db: DBSession = Depends(get_db)):
    """获取已保存的结果"""
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    from scoring import DIAGNOSIS, THRESHOLD
    quadrant_label, _ = DIAGNOSIS[session.quadrant]

    return ResultResponse(
        session_id=session.id,
        age=session.age,
        quadrant=session.quadrant,
        quadrant_label=quadrant_label,
        diagnosis=session.diagnosis,
        chart_data=ChartData(
            us_score=session.us_total_score,
            cn_score=session.cn_total_score,
            threshold=THRESHOLD,
        ),
        created_at=session.created_at.isoformat(),
    )


@app.get("/api/export/{session_id}")
def export_pdf(session_id: str, db: DBSession = Depends(get_db)):
    """导出 PDF 报告"""
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    from scoring import DIAGNOSIS, THRESHOLD
    quadrant_label, _ = DIAGNOSIS[session.quadrant]

    pdf_bytes = generate_pdf({
        "session_id": session.id,
        "age": session.age,
        "us_total_score": session.us_total_score,
        "cn_total_score": session.cn_total_score,
        "quadrant": session.quadrant,
        "quadrant_label": quadrant_label,
        "diagnosis": session.diagnosis,
        "created_at": session.created_at.strftime("%Y-%m-%d %H:%M"),
    })

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{session_id[:8]}.pdf"},
    )
