from langgraph.graph import StateGraph
from src.agents.orchestator.state import OrchestratorState

from src.agents.orchestator.nodes import (
    orchestrator_start,
    orchestrator_before_round,
    orchestrator_after_round,
    orchestrator_end,
)
from src.agents.entrepreneur.nodes import (
    entrepreneur_pitch,
    entrepreneur_concession,
    entrepreneur_evaluate_offers,
)
from src.agents.judge.nodes import (
    judges_evaluate_pitch,
    judges_update_round,
    judges_make_offers,
)
from src.agents.orchestator.nodes import dialogue_round


def build_simulation_graph():
    g = StateGraph(OrchestratorState)

    # === NODOS BASE ===
    g.add_node("start", orchestrator_start)
    g.add_node("pitch", entrepreneur_pitch)
    g.add_node("judge_initial_eval", judges_evaluate_pitch)
    g.add_node("before_round", orchestrator_before_round)
    g.add_node("judge_round_update", judges_update_round)
    g.add_node("dialogue_round", dialogue_round)  # NUEVO nodo de diálogo
    g.add_node("judge_offers", judges_make_offers)
    g.add_node("entrepreneur_concession", entrepreneur_concession)
    g.add_node("entrepreneur_eval_offers", entrepreneur_evaluate_offers)
    g.add_node("after_round", orchestrator_after_round)
    g.add_node("end", orchestrator_end)

    # === FLUJO ===
    g.add_edge("start", "pitch")
    g.add_edge("pitch", "judge_initial_eval")

    g.add_conditional_edges(
        "judge_initial_eval",
        lambda s: "end" if s.get("finished") else "continue",
        path_map={"end": "end", "continue": "before_round"},
    )

    g.add_conditional_edges(
        "before_round",
        lambda s: "end" if s.get("finished") else "continue",
        path_map={"end": "end", "continue": "judge_round_update"},
    )

    g.add_edge("judge_round_update", "dialogue_round")
    g.add_edge("dialogue_round", "judge_offers")
    g.add_edge("judge_offers", "entrepreneur_concession")
    g.add_edge("entrepreneur_concession", "entrepreneur_eval_offers")

    g.add_conditional_edges(
        "entrepreneur_eval_offers",
        lambda s: "end" if s.get("finished") else "continue",
        path_map={"end": "end", "continue": "after_round"},
    )

    g.add_edge("after_round", "before_round")

    g.set_entry_point("start")
    g.set_finish_point("end")

    return g
