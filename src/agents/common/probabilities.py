from typing import List, Dict, Any

from src.agents.common.math import sigmoid


def judge_success_probability(judge: Dict[str, Any]) -> float:
    interest = float(judge.get("current_interest_level", 0.0))
    trust = float(judge.get("trust_in_entrepreneur", 0.5))
    risk = float(judge.get("perceived_risk_score", 0.5))
    upside = float(judge.get("perceived_upside_score", 0.5))

    x = interest + trust - risk + upside
    return sigmoid(x)


def simulation_success_probability(judges: List[Dict[str, Any]]) -> float:
    p_no_deal = 1.0
    for j in judges:
        p_j = judge_success_probability(j)
        p_no_deal *= (1.0 - p_j)
    return 1.0 - p_no_deal