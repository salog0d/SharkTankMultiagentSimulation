from typing import TypedDict, List, Dict, Tuple, Any
from src.agents.common.phases import PHASES
from src.agents.common.types import AnswerQualityLogEntry, ErrorEntry


class EntrepreneurState(TypedDict, total=False):
    phase: PHASES

    # Pitch data
    name: str
    description: str
    target_market: str
    revenue_model: str
    current_traction: str
    investment_needed: float
    use_of_funds: str

    stage: str
    valuation_ask: float
    equity_offered: float
    monthly_revenue: float
    monthly_burn: float
    gross_margin: float | None

    team_size: int
    founder_experience_score: float
    tech_moat_score: float
    competition_intensity_score: float
    regulatory_risk_score: float

    exit_strategy: str
    growth_strategy: str
    use_of_funds_breakdown: Dict[str, float]

    # Dynamic
    negotiations: List[str]
    answers_log: List[AnswerQualityLogEntry]
    concessions_history: List[Dict[str, float | str]]

    # Narrative
    narrative_pitch: str
    inner_narratives: List[Dict[str, Any]]  # <- NUEVO

    # Verdict
    verdict_expanded: Tuple[bool, str]
    verdict: bool

    # Errors
    errors: List[ErrorEntry]
