from datetime import datetime
from typing import Dict, Any, List

from src.agents.entrepreneur.dynamics import (
    concession_effect,
    entrepreneur_acceptance_probability,
)
from src.agents.common.llm import LLM
from src.agents.entrepreneur.prompts import (
    ENTREPRENEUR_PITCH_PROMPT,
    ENTREPRENEUR_CONCESSION_PROMPT,
    ENTREPRENEUR_OFFER_REACTION_PROMPT,
)


def _append_log(state: Dict[str, Any], entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    logs = list(state.get("event_log", []))
    logs.append(entry)
    return logs


async def entrepreneur_pitch(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    logs = list(state.get("event_log", []))

    prompt = ENTREPRENEUR_PITCH_PROMPT.format(data=ent)
    narrative = await LLM.generate(prompt)
    ent["narrative_pitch"] = narrative

    logs.append(
        {
            "event": "pitch_narrative",
            "text": narrative,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    return {
        "entrepreneur": ent,
        "event_log": logs,
    }


async def entrepreneur_concession(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    judges = state["judges"]
    logs = list(state.get("event_log", []))
    strength = 0.3

    for j in judges:
        delta = concession_effect(ent, j, strength)
        j["current_interest_level"] = min(
            1.0,
            j.get("current_interest_level", 0.0) + delta * 0.1,
        )

    prompt = ENTREPRENEUR_CONCESSION_PROMPT.format(
        data={"strength": strength, "entrepreneur": ent},
    )
    narrative = await LLM.generate(prompt)

    ent.setdefault("concessions_history", []).append(
        {
            "round": state.get("round", 0),
            "strength": strength,
            "narrative": narrative,
        }
    )

    logs.append(
        {
            "event": "entrepreneur_concession",
            "round": state.get("round", 0),
            "strength": strength,
            "narrative": narrative,
        }
    )

    return {
        "entrepreneur": ent,
        "judges": judges,
        "event_log": logs,
    }


async def entrepreneur_evaluate_offers(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    judges = state["judges"]
    logs = list(state.get("event_log", []))
    finished = bool(state.get("finished", False))

    for j in judges:
        for offer in j.get("offers_made", []):
            prompt = ENTREPRENEUR_OFFER_REACTION_PROMPT.format(
                offer=offer,
                entrepreneur=ent,
            )
            reaction = await LLM.generate(prompt)

            logs.append(
                {
                    "event": "entrepreneur_offer_reaction",
                    "judge": j.get("name"),
                    "offer": offer,
                    "reaction": reaction,
                }
            )

            p_accept = entrepreneur_acceptance_probability(ent, offer)
            if p_accept > 0.6:
                finished = True
                logs.append(
                    {
                        "event": "offer_accepted",
                        "judge": j.get("name"),
                        "offer": offer,
                        "probability": p_accept,
                    }
                )
                break
        if finished:
            break

    return {
        "entrepreneur": ent,
        "judges": judges,
        "event_log": logs,
        "finished": finished,
    }
