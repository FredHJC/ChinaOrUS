import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    age = Column(Integer, nullable=False)
    us_total_score = Column(Float, nullable=False)
    cn_total_score = Column(Float, nullable=False)
    quadrant = Column(String, nullable=False)
    diagnosis = Column(Text, nullable=False)

    answers = relationship("Answer", back_populates="session", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False)
    question_id = Column(Integer, nullable=False)
    selected_option = Column(String, nullable=False)
    weight = Column(Integer, nullable=False)

    session = relationship("Session", back_populates="answers")
