from src.agents.globalState import PHASES
from typing import TypedDict, Callable, Awaitable, List, Dict, Any, Tuple

class JudgeState(TypedDict, total=False):

    # LangGraph emit signature
    Emit: Callable[[str, Any], Awaitable[None]]

    # Phase
    phase: PHASES

    # ----------------------------
    # Investor Profile (static)
    # ----------------------------
    risk_tolerance: float                  # 0–1
    return_target: float                   # expected ROI % (0.0–1.0)
    scalability_focus: float               # 0–1
    negotiation_aggressiveness: float      # 0–1
    showmanship_preference: float          # 0–1

    sector_preference: List[str]           # ["fintech", "healthtech", ...]
    ticket_min: float                      # min investment ($)
    ticket_max: float                      # max investment ($)
    time_horizon_years: float              # exit horizon
    impact_focus: float                    # ESG/impact weighting
    control_preference: float              # how much ownership they want (0–1)

    # ----------------------------
    # Dynamic Evaluation Variables
    # ----------------------------
    allocated_budget_remaining: float
    current_interest_level: float          # 0–1
    trust_in_entrepreneur: float           # 0–1
    perceived_risk_score: float            # calculated by judge tools
    perceived_upside_score: float          # calculated by judge tools

    offers_made: List[Dict[str, Any]]
    deal_breakers_triggered: List[str]

    # ----------------------------
    # Entrepreneur Pitch Data
    # (the judge needs a local view of these)
    # ----------------------------
    name: str
    description: str
    target_market: str
    revenue_model: str
    current_traction: str
    investment_needed: str
    use_of_funds: str
    market_similar_prices: List[int]

    negociations: List[str]

    # Verdict
    veredict_expanded: Tuple[bool, str]
    veredict: bool

    # Errors
    errors: List[Dict[str, str]]
