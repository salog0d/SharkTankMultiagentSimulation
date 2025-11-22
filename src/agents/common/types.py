from typing import TypedDict

class AnswerQualityLogEntry(TypedDict):
    question: str
    answer: str
    quality_score: float
    reason: str


class Offer(TypedDict):
    equity: float
    amount: float
    valuation: float


class ErrorEntry(TypedDict):
    error_type: str
    message: str
    timestamp: str
