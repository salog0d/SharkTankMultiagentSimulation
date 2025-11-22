from typing import Dict, Any, List

from src.agents.common.llm import LLM
from src.agents.orchestator.prompts import ROUND_SUMMARY_PROMPT


def _append_log(state: Dict[str, Any], entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    logs = list(state.get("event_log", []))
    logs.append(entry)
    return logs


async def orchestrator_start(state: Dict[str, Any]) -> Dict[str, Any]:
    logs = _append_log(state, {"event": "sim_start"})
    return {"event_log": logs}


async def orchestrator_before_round(state: Dict[str, Any]) -> Dict[str, Any]:
    logs = list(state.get("event_log", []))

    if state.get("finished"):
        return {}

    round_num = int(state.get("round", 0))
    max_rounds = int(state.get("max_rounds", 6))

    if round_num >= max_rounds:
        logs = _append_log(state, {"event": "max_rounds_reached", "round": round_num})
        return {"finished": True, "event_log": logs}

    logs = _append_log(state, {"event": "round_start", "round": round_num})
    return {"event_log": logs}


async def orchestrator_after_round(state: Dict[str, Any]) -> Dict[str, Any]:
    logs = list(state.get("event_log", []))

    # Narrativa global de la ronda
    prompt = ROUND_SUMMARY_PROMPT.format(state=state)
    summary = await LLM.generate(prompt)

    logs.append(
        {
            "event": "round_summary",
            "round": state.get("round", 0),
            "summary": summary,
        }
    )

    updates: Dict[str, Any] = {"event_log": logs}

    if not state.get("finished"):
        updates["round"] = int(state.get("round", 0)) + 1

    return updates


async def orchestrator_end(state: Dict[str, Any]) -> Dict[str, Any]:
    logs = _append_log(
        state,
        {"event": "sim_end", "round": state.get("round", 0)},
    )
    return {"event_log": logs}
