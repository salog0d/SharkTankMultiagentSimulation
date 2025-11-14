from src.agents.globalState import PHASES
from typing import TypedDict, Callable, Awaitable, List, Dict, Any, Tuple

class EntrepreneurState(TypedDict, total=False):

    Emit: Callable[[str, Any], Awaitable[None]]

    # Phase
    phase: PHASES

    # ----------------------------
    # Core Pitch Inputs
    # ----------------------------
    name: str
    description: str
    target_market: str
    revenue_model: str
    current_traction: str
    investment_needed: str
    use_of_funds: str

    # ----------------------------
    # Business Data (optional but powerful)
    # ----------------------------
    stage: str                              # idea/mvp/pre-seed/seed/series_a
    valuation_ask: float
    equity_offered: float                   # 0–1
    monthly_revenue: float
    monthly_burn: float
    runway_months: float
    cac: float | None
    ltv: float | None
    gross_margin: float | None

    team_size: int
    founder_experience_score: float
    tech_moat_score: float
    competition_intensity_score: float
    regulatory_risk_score: float

    exit_strategy: str
    growth_strategy: str
    use_of_funds_breakdown: Dict[str, float]

    # ----------------------------
    # Dynamic Feedback From Judges
    # ----------------------------
    negociations: List[str]
    answers_quality_log: List[Dict[str, Any]]
    concessions_history: List[str]

    # Verdict
    veredict_expanded: Tuple[bool, str]
    veredict: bool

    # Errors
    errors: List[Dict[str, str]]
