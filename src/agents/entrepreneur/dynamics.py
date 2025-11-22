from typing import Dict, Any

from src.agents.common.math import clamp


def concession_effect(ent: Dict[str, Any],
                      judge: Dict[str, Any],
                      concession_strength: float) -> float:
    """
    Efecto neto en el clima de negociación.
    concession_strength ∈ [0,1]
    """
    concession_strength = max(0.0, min(1.0, concession_strength))
    base_gain = 0.8 * concession_strength
    trust_boost = 0.3 * concession_strength
    aggr = float(judge.get("negotiation_aggressiveness", 0.5) or 0.5)
    fatigue_penalty = -0.1 * aggr * concession_strength
    return clamp(base_gain + trust_boost + fatigue_penalty)


def entrepreneur_acceptance_probability(
    ent: Dict[str, Any],
    offer: Dict[str, float],
) -> float:
    equity = float(offer.get("equity", 0.0) or 0.0)
    valuation = float(offer.get("valuation", 0.0) or 0.0)
    ask_val = float(ent.get("valuation_ask", valuation) or valuation)

    if ask_val <= 0:
        ask_val = valuation or 1.0

    valuation_gap = ask_val - valuation

    if valuation_gap <= 0:
        base = 0.9 - equity * 0.5
        return max(0.0, min(1.0, base))

    stubbornness = 1.0 - float(ent.get("founder_experience_score", 0.5) or 0.5)
    base = 0.4 - (valuation_gap / ask_val) * stubbornness
    return max(0.0, min(1.0, base))