import asyncio
from src.agents.orchestator.graph import build_simulation_graph
from initial_state import initial_state
from src.core.settings import settings


def print_dialogue(event):
    t = event.get("type")
    data = event.get("data", {})

    if t != "on_channel":
        return

    if data.get("channel") != "log":
        return

    payload = data.get("data", {})
    event_type = payload.get("event")

    # Pitch del emprendedor
    if event_type == "pitch_narrative":
        print(f"\n[SALO → SHARKS]: {payload.get('text')}\n")

    # Evaluación inicial de jueces
    elif event_type == "judge_evaluation":
        judge = payload.get("judge")
        print(f"[{judge}]: {payload.get('evaluation')}")

    # Ofertas con narrativa
    elif event_type == "offer_made":
        judge = payload.get("judge")
        offer = payload.get("offer")
        narrative = payload.get("narrative")
        print(f"\n[{judge} - OFFER]: {offer}")
        print(f"[{judge} - WHY]: {narrative}")

    # Concesión del emprendedor
    elif event_type == "entrepreneur_concession":
        print(f"\n[SALO (Concesión)]: {payload.get('narrative')}")

    # Reacción a ofertas
    elif event_type == "entrepreneur_offer_reaction":
        judge = payload.get("judge")
        reaction = payload.get("reaction")
        print(f"[SALO → {judge}]: {reaction}")

    # Resumen de ronda
    elif event_type == "round_summary":
        print(f"\n[ROUND SUMMARY]: {payload.get('summary')}\n")


async def main():
    graph = build_simulation_graph()
    app = graph.compile()

    print("USING MODEL:", settings.azure_deployment)
    print("\n=== CONVERSACIÓN ===\n")

    async for event in app.astream_events(initial_state):
        print_dialogue(event)

    print("\n=== FINAL STATE ===")
    final_state = await app.ainvoke(initial_state)
    print(final_state)


if __name__ == "__main__":
    asyncio.run(main())
