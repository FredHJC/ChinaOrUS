from pydantic import BaseModel, Field


class DualAnswerItem(BaseModel):
    question_id: int = Field(..., ge=4, le=12)
    us_tier: int = Field(..., ge=1, le=5)
    cn_tier: int = Field(..., ge=1, le=5)
    weight: int = Field(..., ge=1, le=5)


class SingleAnswerItem(BaseModel):
    question_id: int = Field(..., ge=0, le=28)
    selected_option: str = Field(..., pattern=r"^[A-E]$")
    weight: int = Field(..., ge=1, le=5)


class SubmitRequest(BaseModel):
    dual_answers: list[DualAnswerItem] = Field(..., min_length=9, max_length=9)
    single_answers: list[SingleAnswerItem] = Field(..., min_length=20, max_length=20)


class ChartData(BaseModel):
    us_score: float
    cn_score: float
    threshold: float


class SubmitResponse(BaseModel):
    session_id: str
    quadrant: str
    quadrant_label: str
    diagnosis: str
    chart_data: ChartData


class ScatterPointOut(BaseModel):
    us_score: float
    cn_score: float
    quadrant: str


class ResultResponse(BaseModel):
    session_id: str
    quadrant: str
    quadrant_label: str
    diagnosis: str
    chart_data: ChartData
    created_at: str
