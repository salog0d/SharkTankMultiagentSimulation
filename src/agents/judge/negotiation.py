from typing import Dict, Any

from src.agents.common.math import clamp, sigmoid
from src.agents.entrepreneur.scoring import moat_strength_score
from src.agents.judge.scoring import (
    perceived_risk,
    perceived_upside,
    competition_pressure_score,
    base_interest_signal,
)


def judge_fatigue_increment(judge: Dict[str, Any]) -> float:
    aggr = float(judge.get("negotiation_aggressiveness", 0.5) or 0.5)
    return 0.1 + aggr * 0.15


def update_trust(judge: Dict[str, Any], ent: Dict[str, Any], round_num: int) -> float:
    base = float(judge.get("trust_in_entrepreneur", 0.5) or 0.5)
    delta = (
        0.1 * moat_strength_score(ent)
        - 0.1 * perceived_risk(ent, judge)
        - 0.04 * judge_fatigue_increment(judge)
    )
    new_trust = clamp(base + delta)
    judge["trust_in_entrepreneur"] = new_trust
    return new_trust


def update_interest_after_round(judge: Dict[str, Any], ent: Dict[str, Any]) -> float:
    x = (
        base_interest_signal(judge, ent)
        - 1.3 * perceived_risk(ent, judge)
        + 1.2 * perceived_upside(ent, judge)
        + 0.6 * moat_strength_score(ent)
        - 0.4 * competition_pressure_score(ent)
        - 0.4 * judge_fatigue_increment(judge)
    )
    new_interest = round(sigmoid(x), 4)
    judge["current_interest_level"] = new_interest
    return new_interest


def ready_to_offer(judge: Dict[str, Any]) -> bool:
    interest = float(judge.get("current_interest_level", 0.0) or 0.0)
    trust = float(judge.get("trust_in_entrepreneur", 0.5) or 0.5)
    risk = float(judge.get("perceived_risk_score", 0.5) or 0.5)
    score = interest + trust - risk
    return score > 1.2