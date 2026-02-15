from typing import Optional

from pydantic import BaseModel, Field


class DualAnswerItem(BaseModel):
    question_id: int = Field(..., ge=1, le=9)
    us_tier: int = Field(..., ge=1, le=5)
    cn_tier: int = Field(..., ge=1, le=5)
    weight: int = Field(..., ge=1, le=5)


class SingleAnswerItem(BaseModel):
    question_id: int = Field(..., ge=10, le=25)
    selected_option: str = Field(..., pattern=r"^[A-E]$")
    weight: int = Field(..., ge=1, le=5)


class SubmitRequest(BaseModel):
    age: int = Field(..., ge=20)  # 无上限，35+ 后端归类
    dual_answers: list[DualAnswerItem] = Field(..., min_length=9, max_length=9)
    single_answers: list[SingleAnswerItem] = Field(..., min_length=16, max_length=16)


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
    age: int
    quadrant: str
    quadrant_label: str
    diagnosis: str
    chart_data: ChartData
    created_at: str
