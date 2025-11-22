from typing import Dict, Any, List
import random

from src.agents.common.math import clamp


def generate_offer(judge: Dict[str, Any], ent: Dict[str, Any]) -> Dict[str, float]:
    interest = float(judge.get("current_interest_level", 0.0) or 0.0)
    risk = float(judge.get("perceived_risk_score", 0.5) or 0.5)

    equity = clamp(0.25 - interest * 0.1 + risk * 0.05, 0.02, 0.35)

    ticket_min = float(judge.get("ticket_min", 50_000.0) or 50_000.0)
    ticket_max = float(judge.get("ticket_max", 250_000.0) or 250_000.0)
    ticket = random.uniform(ticket_min, ticket_max)

    valuation = ticket / equity if equity > 0 else ticket
    return {
        "equity": round(equity, 3),
        "amount": round(ticket, 2),
        "valuation": round(valuation, 2),
    }


def deal_breaker_triggered(judge: Dict[str, Any], ent: Dict[str, Any]) -> List[str]:
    breakers: List[str] = []

    if float(ent.get("monthly_burn", 0.0) or 0.0) > 150_000.0:
        breakers.append("burn_too_high")

    if float(ent.get("gross_margin", 0.2) or 0.2) < 0.15:
        breakers.append("margin_too_low")

    if float(ent.get("competition_intensity_score", 0.7) or 0.7) > 0.85:
        breakers.append("competition_too_high")

    if (
        float(judge.get("control_preference", 0.0) or 0.0) > 0.8
        and float(ent.get("equity_offered", 0.0) or 0.0) < 0.15
    ):
        breakers.append("no_control")

    return breakers