from typing import Dict, Any
from math import log1p

from src.agents.common.math import clamp
from src.agents.entrepreneur.scoring import (
    traction_score,
    economic_sanity
)


def founder_fit(judge: Dict[str, Any], ent: Dict[str, Any]) -> float:
    exp = float(ent.get("founder_experience_score", 0.0) or 0.0)
    risk_tol = float(judge.get("risk_tolerance", 0.5) or 0.5)
    return clamp(exp * (0.7 + risk_tol))


def sector_alignment(judge: Dict[str, Any], ent: Dict[str, Any]) -> float:
    prefs = [s.lower() for s in judge.get("sector_preference", [])]
    desc = str(ent.get("description", "")).lower()
    aligned = any(s in desc for s in prefs)
    return 1.5 if aligned else -0.3


def perceived_risk(ent: Dict[str, Any], judge: Dict[str, Any]) -> float:
    comp = float(ent.get("competition_intensity_score", 0.5) or 0.5)
    reg = float(ent.get("regulatory_risk_score", 0.5) or 0.5)
    burn = float(ent.get("monthly_burn", 0.0) or 0.0)
    margin = float(ent.get("gross_margin", 0.3) or 0.3)

    structural = comp + reg + (burn / 100000.0) - margin
    risk_tol = float(judge.get("risk_tolerance", 0.5) or 0.5)

    return structural * (1.2 - risk_tol)


def perceived_upside(ent: Dict[str, Any], judge: Dict[str, Any]) -> float:
    margin = float(ent.get("gross_margin", 0.3) or 0.3)
    revenue = float(ent.get("monthly_revenue", 0.0) or 0.0)
    upside = (
        margin * 1.5
        + log1p(revenue) * 0.3
        + float(ent.get("tech_moat_score", 0.4) or 0.4) * 0.7
    )
    return clamp(upside)


def competition_pressure_score(ent: Dict[str, Any]) -> float:
    comp = float(ent.get("competition_intensity_score", 0.5) or 0.5)
    return clamp(-comp)


def base_interest_signal(judge: Dict[str, Any], ent: Dict[str, Any]) -> float:
    x = (
        1.4 * traction_score(ent)
        + 1.0 * economic_sanity(ent)
        + 1.0 * founder_fit(judge, ent)
        + 0.8 * sector_alignment(judge, ent)
    )
    return x
