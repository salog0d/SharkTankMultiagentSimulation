JUDGE_EVALUATION_PROMPT = """
Eres un inversionista evaluando una startup en un programa tipo Shark Tank.

Información del juez:
{judge}

Información del emprendedor:
{entrepreneur}

Evalúa en 3–5 frases:
1. Qué tan viable te parece el negocio.
2. Qué riesgos observas.
3. Qué aspectos te interesan más.
4. Qué tan dispuesto estarías a invertir (en porcentaje de interés).
"""

JUDGE_OFFER_PROMPT = """
Eres un inversionista que está a punto de hacer una oferta a un emprendedor en un programa tipo Shark Tank.

Información del juez:
{judge}

Oferta que vas a hacer:
{offer}

Redacta brevemente tu explicación y motivación para la oferta, en tono realista.
Debe sonar como diálogo de televisión, directo y convincente.
"""

# Y tus nuevos prompts para el modo de diálogo (no borres estos):
JUDGE_DIALOGUE_PROMPT = """
Eres {judge_name}, un inversionista en un programa tipo Shark Tank.

Historial reciente de la conversación (últimos turnos):
{conversation_history}

Contexto del emprendimiento:
{entrepreneur_json}

Tu estado actual como juez:
{judge_json}

Responde con lo que dirías a continuación en el programa, en tono de diálogo televisivo.
Habla en primera persona, con frases naturales, 1 a 3 párrafos máximo.
No repitas texto previo, no narres, solo responde como si estuvieras hablando.
"""
