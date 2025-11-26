from typing import Dict, Any, List

from src.agents.common.llm import LLM
from src.agents.orchestator.prompts import ROUND_SUMMARY_PROMPT
import json
from typing import Dict, Any, List
from src.agents.common.llm import LLM
from src.agents.judge.prompts import JUDGE_DIALOGUE_PROMPT
from src.agents.entrepreneur.prompts import ENTREPRENEUR_DIALOGUE_PROMPT

async def dialogue_round(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simula un diálogo back-and-forth entre los jueces y el emprendedor.
    Cada juez hace un comentario basado en el historial reciente,
    y luego el emprendedor responde a todos.
    """
    ent = state["entrepreneur"]
    judges = state["judges"]
    history = list(state.get("conversation_history", []))
    logs = list(state.get("event_log", []))

    # === JUECES HABLAN ===
    for j in judges:
        prompt = JUDGE_DIALOGUE_PROMPT.format(
            judge_name=j["name"],
            entrepreneur_json=json.dumps(ent, ensure_ascii=False),
            judge_json=json.dumps(j, ensure_ascii=False),
            conversation_history=json.dumps(history[-6:], ensure_ascii=False),
        )

        response = await LLM.generate(prompt)

        # Guardar en logs y conversación
        logs.append({
            "event": "dialogue_turn",
            "role": "judge",
            "speaker": j["name"],
            "text": response,
        })
        history.append({
            "role": "judge",
            "speaker": j["name"],
            "text": response,
        })

    # === EMPRENDEDOR RESPONDE ===
    prompt = ENTREPRENEUR_DIALOGUE_PROMPT.format(
        entrepreneur_name=ent["name"],
        entrepreneur_json=json.dumps(ent, ensure_ascii=False),
        conversation_history=json.dumps(history[-6:], ensure_ascii=False),
    )

    ent_response = await LLM.generate(prompt)

    logs.append({
        "event": "dialogue_turn",
        "role": "entrepreneur",
        "speaker": ent["name"],
        "text": ent_response,
    })
    history.append({
        "role": "entrepreneur",
        "speaker": ent["name"],
        "text": ent_response,
    })

    return {
        "conversation_history": history,
        "event_log": logs,
    }


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
