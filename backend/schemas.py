from pydantic import BaseModel, Field


class AnswerItem(BaseModel):
    question_id: int = Field(..., ge=1, le=24)
    selected_option: str = Field(..., pattern=r"^[A-C]$")
    weight: int = Field(..., ge=1, le=5)


class SubmitRequest(BaseModel):
    age: int = Field(..., ge=20, le=35)
    age_weight: int = Field(..., ge=1, le=5)
    answers: list[AnswerItem] = Field(..., min_length=24, max_length=24)


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


class ResultResponse(BaseModel):
    session_id: str
    age: int
    quadrant: str
    quadrant_label: str
    diagnosis: str
    chart_data: ChartData
    created_at: str
