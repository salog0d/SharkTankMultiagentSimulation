import asyncio
from src.agents.orchestator.graph import build_simulation_graph
from initial_state import initial_state
from src.core.settings import settings


def print_dialogue(event):
    t = event.get("type")
    data = event.get("data", {})

    # Solo nos interesan eventos mandados por el canal "log"
    if t != "on_channel":
        return

    if data.get("channel") != "log":
        return

    payload = data.get("data", {})
    event_type = payload.get("event")

    # === NUEVO: diálogo genérico (jueces <-> emprendedor) ===
    if event_type == "dialogue_turn":
        role = payload.get("role")
        speaker = payload.get("speaker", "UNKNOWN")
        text = payload.get("text", "")

        if role == "entrepreneur":
            # Emprendedor hablando hacia los sharks
            print(f"\n[SALO → SHARKS]: {text}\n")
        else:
            # Cualquier juez u otro rol
            print(f"[{speaker}]: {text}\n")

    # === Eventos antiguos que sigue generando tu grafo ===
    # Pitch del emprendedor
    elif event_type == "pitch_narrative":
        print(f"\n[SALO → SHARKS]: {payload.get('text')}\n")

    # Evaluación inicial de jueces
    elif event_type == "judge_evaluation":
        judge = payload.get("judge")
        print(f"[{judge}]: {payload.get('evaluation')}\n")

    # Ofertas con narrativa
    elif event_type == "offer_made":
        judge = payload.get("judge")
        offer = payload.get("offer")
        narrative = payload.get("narrative")
        print(f"\n[{judge} - OFFER]: {offer}")
        print(f"[{judge} - WHY]: {narrative}\n")

    # Concesión del emprendedor
    elif event_type == "entrepreneur_concession":
        print(f"\n[SALO (Concesión)]: {payload.get('narrative')}\n")

    # Reacción a ofertas
    elif event_type == "entrepreneur_offer_reaction":
        judge = payload.get("judge")
        reaction = payload.get("reaction")
        print(f"[SALO → {judge}]: {reaction}\n")

    # Resumen de ronda
    elif event_type == "round_summary":
        print(f"\n[ROUND SUMMARY]: {payload.get('summary')}\n")


def print_final_summary(state: dict) -> None:
    ent = state["entrepreneur"]
    judges = state["judges"]
    event_log = state.get("event_log", [])

    print("\n==============================")
    print("🏁  RESUMEN FINAL DEL PROGRAMA")
    print("==============================\n")

    # --- Startup ---
    print("💼 STARTUP")
    print(f"  Nombre: {ent.get('name')}")
    print(f"  Etapa: {ent.get('stage')}")
    print(f"  Valuación objetivo: ${ent.get('valuation_ask'):,}")
    print(f"  Equity ofrecido inicial: {ent.get('equity_offered')*100:.1f}%")
    print(f"  Inversión buscada: ${ent.get('investment_needed'):,}")
    print(f"  Ingresos mensuales: ${ent.get('monthly_revenue'):,}")
    print(f"  Burn mensual: ${ent.get('monthly_burn'):,}")
    print(f"  Tracción: {ent.get('current_traction')}")
    print()

    # --- Ofertas finales ---
    print("💰 OFERTAS DE JUECES")
    for j in judges:
        name = j.get("name", "Unknown")
        offers = j.get("offers_made", [])
        if not offers:
            print(f"  🦈 {name}: no hizo oferta.")
            continue
        for o in offers:
            amount = o.get("amount", 0.0)
            equity = o.get("equity", 0.0) * 100
            valuation = o.get("valuation", 0.0)
            print(
                f"  🦈 {name}: ${amount:,.2f} por {equity:.1f}% "
                f"(valuación implícita: ${valuation:,.0f})"
            )
    print()

    # --- Concesiones del emprendedor ---
    print("🤝 CONCESIONES DEL EMPRENDEDOR")
    concessions = ent.get("concessions_history", [])
    if not concessions:
        print("  Sin concesiones registradas.\n")
    else:
        for c in concessions:
            rnd = c.get("round")
            narrative = c.get("narrative", "")
            snippet = narrative.replace("\n", " ")
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            print(f"  Ronda {rnd}: {snippet}")
        print()

    # --- Resumen de ronda (si existe) ---
    summaries = [
        e for e in event_log if e.get("event") == "round_summary"
    ]
    if summaries:
        last_summary = summaries[-1]
        print("📊 RESUMEN DE LA RONDA (LLM)")
        print(last_summary.get("summary", ""))
        print()

    # --- Estado de simulación ---
    print("✅ ESTADO DE LA SIMULACIÓN")
    print(f"  Rondas ejecutadas: {state.get('round')}")
    print(f"  Finalizado: {'Sí' if state.get('finished') else 'No'}")
    print("==============================\n")

    # --- Conversación reconstruida desde event_log ---
    print("🎬 REPLAY DE LA CONVERSACIÓN (desde event_log)\n")
    for e in event_log:
        ev = e.get("event")
        if ev == "pitch_narrative":
            print("[SALO → SHARKS]:")
            print(e.get("text", ""), "\n")
        elif ev == "judge_evaluation":
            print(f"[{e.get('judge')} - Evaluación]:")
            print(e.get("evaluation", ""), "\n")
        elif ev == "dialogue_turn":
            role = e.get("role")
            speaker = e.get("speaker", "UNKNOWN")
            text = e.get("text", "")
            if role == "entrepreneur":
                print(f"[SALO → SHARKS]: {text}\n")
            else:
                print(f"[{speaker}]: {text}\n")
        elif ev == "offer_made":
            judge = e.get("judge")
            offer = e.get("offer", {})
            narrative = e.get("narrative", "")
            print(f"[{judge} - OFFER]: {offer}")
            print(f"[{judge} - WHY]: {narrative}\n")
        elif ev == "entrepreneur_concession":
            print("[SALO (Concesión)]:")
            print(e.get("narrative", ""), "\n")
        elif ev == "entrepreneur_offer_reaction":
            judge = e.get("judge")
            print(f"[SALO → {judge}]:")
            print(e.get("reaction", ""), "\n")
        # round_summary ya lo imprimimos arriba si quieres dejarlo solo ahí


async def main():
    graph = build_simulation_graph()
    app = graph.compile()

    print("USING MODEL:", settings.azure_deployment)
    print("\n=== CONVERSACIÓN (STREAM) ===\n")

    async for event in app.astream_events(initial_state):
        print_dialogue(event)

    print("\n=== FINAL STATE (FORMATEADO) ===")
    final_state = await app.ainvoke(initial_state)
    print_final_summary(final_state)


if __name__ == "__main__":
    asyncio.run(main())
