from pydantic import BaseModel
from src.v1.core.config import QUESTION_ANSWER_MODEL


class QAPredictionResult(BaseModel):

    score: float
    start: int
    end: int
    answer: str
    model: str = QUESTION_ANSWER_MODEL
