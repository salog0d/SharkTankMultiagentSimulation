from typing import Dict, Any
from math import log1p

from src.agents.common.math import clamp


def traction_score(ent: Dict[str, Any]) -> float:
    revenue = float(ent.get("monthly_revenue", 0.0) or 0.0)
    burn = float(ent.get("monthly_burn", 1.0) or 1.0)
    margin = float(ent.get("gross_margin", 0.2) or 0.2)

    traction = (revenue / (burn + 1.0)) * 0.6 + margin * 0.4
    return clamp(traction)


def economic_sanity(ent: Dict[str, Any]) -> float:
    valuation = float(ent.get("valuation_ask", 0.0) or 0.0)
    revenue = float(ent.get("monthly_revenue", 0.0) or 0.0)

    if revenue <= 0:
        return -3.0

    ratio = valuation / (revenue * 12.0)

    if ratio > 40.0:
        return -3.0
    if ratio > 20.0:
        return -2.0
    if ratio > 10.0:
        return -1.0
    if ratio > 5.0:
        return 0.0
    return 1.0


def team_strength_score(ent: Dict[str, Any]) -> float:
    size = int(ent.get("team_size", 1) or 1)
    exp = float(ent.get("founder_experience_score", 0.5) or 0.5)
    score = (size / 5.0) * 0.5 + exp * 0.5
    return clamp(score)


def moat_strength_score(ent: Dict[str, Any]) -> float:
    moat = float(ent.get("tech_moat_score", 0.3) or 0.3)
    return clamp(moat * 1.2)


def growth_potential_score(ent: Dict[str, Any]) -> float:
    margin = float(ent.get("gross_margin", 0.3) or 0.3)
    revenue = float(ent.get("monthly_revenue", 0.0) or 0.0)
    score = margin * 1.5 + log1p(revenue) * 0.2
    return clamp(score)
