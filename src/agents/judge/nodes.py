from typing import Dict, Any, List

from src.agents.judge.negotiation import (
    update_interest_after_round,
    update_trust,
    ready_to_offer,
)
from src.agents.judge.offers import generate_offer
from src.agents.judge.scoring import perceived_risk, perceived_upside
from src.agents.common.llm import LLM
from src.agents.judge.prompts import (
    JUDGE_EVALUATION_PROMPT,
    JUDGE_OFFER_PROMPT,
)


def _append_log(state: Dict[str, Any], entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    logs = list(state.get("event_log", []))
    logs.append(entry)
    return logs


async def judges_evaluate_pitch(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    judges = state["judges"]
    logs = list(state.get("event_log", []))

    for j in judges:
        j["perceived_risk_score"] = perceived_risk(ent, j)
        j["perceived_upside_score"] = perceived_upside(ent, j)

        prompt = JUDGE_EVALUATION_PROMPT.format(
            judge=j,
            entrepreneur=ent,
        )
        narrative = await LLM.generate(prompt)
        j.setdefault("narrative_evaluations", []).append(narrative)

        logs.append(
            {
                "event": "judge_evaluation",
                "judge": j.get("name"),
                "evaluation": narrative,
            }
        )

    return {
        "judges": judges,
        "event_log": logs,
    }


async def judges_update_round(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    judges = state["judges"]
    logs = list(state.get("event_log", []))

    for j in judges:
        update_trust(j, ent, state.get("round", 0))
        update_interest_after_round(j, ent)

    logs.append(
        {
            "event": "judges_update_round",
            "round": state.get("round", 0),
        }
    )

    return {
        "judges": judges,
        "event_log": logs,
    }


async def judges_make_offers(state: Dict[str, Any]) -> Dict[str, Any]:
    ent = state["entrepreneur"]
    judges = state["judges"]
    logs = list(state.get("event_log", []))

    for j in judges:
        if ready_to_offer(j):
            offer = generate_offer(j, ent)
            j.setdefault("offers_made", []).append(offer)

            prompt = JUDGE_OFFER_PROMPT.format(
                judge=j,
                offer=offer,
            )
            narrative = await LLM.generate(prompt)
            j.setdefault("offer_rationales", []).append(narrative)

            logs.append(
                {
                    "event": "offer_made",
                    "judge": j.get("name"),
                    "offer": offer,
                    "narrative": narrative,
                }
            )

    return {
        "judges": judges,
        "event_log": logs,
    }
