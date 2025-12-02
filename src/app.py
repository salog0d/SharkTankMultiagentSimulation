# src/app.py
from typing import Any, Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.orchestator.graph import build_simulation_graph


# ==========================
# 1. Construir grafo una vez
# ==========================
_graph = build_simulation_graph()
_simulation_app = _graph.compile()


# ==========================
# 2. Modelos de entrada/salida
# ==========================
class SimulationRequest(BaseModel):
    initial_state: Dict[str, Any]


class DialogueTurn(BaseModel):
    speaker: str
    text: str
    event_type: Optional[str] = None


class SimulationResponse(BaseModel):
    dialogue: List[DialogueTurn]


# ==========================
# 3. FastAPI app
# ==========================
app = FastAPI(title="SharkTank Simulation API")


def _extract_dialogue_from_event_log(final_state: Dict[str, Any]) -> List[Dict[str, Any]]:
    ent = final_state.get("entrepreneur", {})
    entrepreneur_name = ent.get("name", "Entrepreneur")

    event_log = final_state.get("event_log", []) or []
    dialogue: List[Dict[str, Any]] = []

    for e in event_log:
        ev = e.get("event")
        speaker: str
        text: str

        if ev == "pitch_narrative":
            speaker = entrepreneur_name
            text = e.get("text", "")

        elif ev == "judge_evaluation":
            speaker = e.get("judge", "Judge")
            text = e.get("evaluation", "")

        elif ev == "dialogue_turn":
            role = e.get("role")
            if role == "entrepreneur":
                speaker = entrepreneur_name
            else:
                speaker = e.get("speaker", "UNKNOWN")
            text = e.get("text", "")

        elif ev == "offer_made":
            speaker = e.get("judge", "Judge")
            offer = e.get("offer", {})
            narrative = e.get("narrative", "")
            text = f"OFFER: {offer} | WHY: {narrative}"

        elif ev == "entrepreneur_concession":
            speaker = entrepreneur_name
            text = e.get("narrative", "")

        elif ev == "entrepreneur_offer_reaction":
            speaker = entrepreneur_name
            text = e.get("reaction", "")

        elif ev == "round_summary":
            speaker = "Orchestrator"
            text = e.get("summary", "")

        else:
            continue

        if not text:
            continue

        dialogue.append(
            {
                "speaker": speaker,
                "text": text,
                "event_type": ev,
            }
        )

    return dialogue


@app.post("/simulate", response_model=SimulationResponse)
async def run_simulation(payload: SimulationRequest) -> SimulationResponse:
    """
    Body esperado:
    {
      "initial_state": { ... }
    }
    """
    final_state = await _simulation_app.ainvoke(payload.initial_state)
    dialogue_items = _extract_dialogue_from_event_log(final_state)
    return SimulationResponse(dialogue=[DialogueTurn(**d) for d in dialogue_items])
