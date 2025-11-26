from typing import TypedDict, List, Tuple, Dict, Any
from src.agents.common.phases import PHASES
from src.agents.common.types import Offer, ErrorEntry


class JudgeState(TypedDict, total=False):
    phase: PHASES
    name: str

    # Investor profile
    risk_tolerance: float
    return_target: float
    scalability_focus: float
    negotiation_aggressiveness: float
    showmanship_preference: float

    sector_preference: List[str]
    ticket_min: float
    ticket_max: float
    time_horizon_years: float
    impact_focus: float
    control_preference: float

    allocated_budget_remaining: float

    # Dynamic perceptions
    current_interest_level: float
    trust_in_entrepreneur: float
    perceived_risk_score: float
    perceived_upside_score: float

    negotiations: List[str]
    offers_made: List[Offer]
    deal_breakers_triggered: List[str]

    # Narrative
    narrative_evaluations: List[str]
    offer_rationales: List[str]
    inner_narratives: List[Dict[str, Any]]  # <- NUEVO

    # Verdict
    verdict_expanded: Tuple[bool, str]
    verdict: bool

    # Errors
    errors: List[ErrorEntry]