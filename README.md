## Shark Tank Multiagent Simulation Backend

Sistema de simulación de negociaciones de inversión tipo Shark Tank mediante agentes autónomos basados en modelos de lenguaje de gran escala (LLM). Simula interacciones realistas entre emprendedores e inversionistas utilizando Azure OpenAI y LangGraph para orquestación de agentes multi-turno.

## Descripción

Este proyecto implementa un sistema de simulación multi-agente que replica dinámicas de negociación de inversión características de programas como Shark Tank. El sistema modela el comportamiento de emprendedores e inversionistas mediante agentes LLM que evalúan propuestas de negocio, calculan riesgos y retornos, generan ofertas de inversión y negocian términos de manera autónoma.

La arquitectura utiliza LangGraph para coordinar flujos de conversación complejos entre múltiples agentes, permitiendo simulaciones realistas de múltiples rondas de negociación con evaluaciones cuantitativas de riesgo, tracción empresarial, ajuste de valuación y dinámica de confianza entre partes. El sistema genera narrativas completas de pitch, evaluaciones de jueces, ofertas estructuradas y concesiones del emprendedor basándose en perfiles de comportamiento configurables.

Este tipo de simulación es útil para entrenar modelos de negociación, analizar estrategias de inversión, preparar a emprendedores para presentaciones reales, y estudiar dinámicas de toma de decisiones en entornos de alta presión.

## Tecnologías

- **Python 3.10+**: Lenguaje base del proyecto
- **LangChain 1.1.0**: Framework para aplicaciones LLM
- **LangGraph 1.0.4**: Orquestación de grafos de agentes con flujos condicionales
- **Azure OpenAI Service**: Proveedor de modelos LLM (GPT-4o-mini configurado)
- **FastAPI 0.123.4**: Framework web asíncrono para API REST
- **Pydantic 2.12.5**: Validación de datos y configuración
- **Uvicorn 0.38.0**: Servidor ASGI de alto rendimiento

## Instalación

### Requisitos previos

- Python 3.10 o superior
- Cuenta de Azure con acceso a Azure OpenAI Service
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clonar el repositorio:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Crear entorno virtual:

```bash
python -m venv venv
```

3. Activar entorno virtual:

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Instalar dependencias:

```bash
# Para desarrollo
pip install -r requirements.txt

# Para producción
pip install -r requirements_prod.txt
```

5. Configurar variables de entorno:

```bash
cp .env.example .env
```

Editar `.env` con las credenciales de Azure OpenAI.

## Ejecución

### Simulación standalone

Ejecutar una simulación completa con el estado inicial predefinido:

```bash
python run_simulation.py
```

Este comando ejecuta una simulación usando la configuración en `initial_state.py` e imprime el diálogo completo en consola, seguido de un resumen estructurado de ofertas, concesiones y métricas finales.

### API REST

Iniciar el servidor FastAPI:

```bash
python src/main.py
```

El servidor estará disponible en `http://localhost:8000`. Documentación interactiva en `http://localhost:8000/docs`.

Ejecutar simulación vía API:

```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d @initial_state.json
```

La respuesta contiene un array de `DialogueTurn` con el historial completo de la conversación.

## Tests

Actualmente el proyecto no tiene suite de tests implementada. La carpeta `tests/` está preparada para expansión futura.

## Ejemplos de uso

### Modificar escenario de simulación

Editar `initial_state.py` para cambiar parámetros del emprendedor o jueces:

```python
initial_state = {
    "entrepreneur": {
        "name": "María González (HealthTech Pro)",
        "investment_needed": 500000.0,
        "valuation_ask": 5000000.0,
        "equity_offered": 0.10,
        "monthly_revenue": 120000.0,
        # ... más campos
    },
    "judges": [
        {
            "name": "Judge_A",
            "risk_tolerance": 0.7,  # Más tolerante al riesgo
            "negotiation_aggressiveness": 0.3,  # Menos agresivo
            # ... más campos
        }
    ]
}
```

### Usar la API programáticamente

```python
import httpx
import asyncio

async def run_simulation():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/simulate",
            json={"initial_state": initial_state}
        )
        result = response.json()
        for turn in result["dialogue"]:
            print(f"{turn['speaker']}: {turn['text']}\n")

asyncio.run(run_simulation())
```

## Estructura del proyecto

```
.
├── src/
│   ├── agents/
│   │   ├── common/           # Utilidades compartidas entre agentes
│   │   │   ├── llm.py        # Cliente Azure OpenAI
│   │   │   ├── math.py       # Funciones matemáticas (sigmoid, clamp)
│   │   │   ├── phases.py     # Enumeración de fases de negociación
│   │   │   ├── probabilities.py  # Cálculo de probabilidades de éxito
│   │   │   ├── types.py      # TypedDicts compartidos
│   │   │   └── prompts/      # Prompts del sistema base
│   │   ├── entrepreneur/     # Agente emprendedor
│   │   │   ├── nodes.py      # Nodos del grafo (pitch, concesión, evaluación)
│   │   │   ├── dynamics.py   # Mecánicas de negociación
│   │   │   ├── scoring.py    # Métricas de tracción y viabilidad
│   │   │   ├── prompts.py    # Prompts específicos del emprendedor
│   │   │   └── state.py      # Estado typed del agente
│   │   ├── judge/            # Agente inversionista
│   │   │   ├── nodes.py      # Nodos de evaluación y ofertas
│   │   │   ├── negotiation.py # Lógica de fatiga, trust, interés
│   │   │   ├── offers.py     # Generación de ofertas estructuradas
│   │   │   ├── scoring.py    # Evaluación de riesgo y upside
│   │   │   ├── prompts.py    # Prompts del inversionista
│   │   │   └── state.py      # Estado typed del juez
│   │   └── orchestator/      # Coordinador de simulación
│   │       ├── graph.py      # Construcción del grafo LangGraph
│   │       ├── nodes.py      # Nodos de control (inicio, fin, rondas)
│   │       ├── prompts.py    # Prompts de resumen
│   │       └── state.py      # Estado global de la simulación
│   ├── core/
│   │   └── settings.py       # Configuración de Azure OpenAI desde .env
│   ├── utils/
│   │   └── pdf_to_text/      # Utilidad para extracción de PDFs (no integrada)
│   ├── app.py                # API FastAPI
│   └── main.py               # Entry point del servidor
├── initial_state.py          # Estado inicial de ejemplo (VitaCode)
├── run_simulation.py         # Script CLI para ejecutar simulaciones
├── requirements.txt          # Dependencias de desarrollo
├── requirements_prod.txt     # Dependencias con versiones fijas
├── .env.example              # Plantilla de variables de entorno
└── .gitignore                # Archivos excluidos del repositorio
```

### Componentes clave

- **`src/agents/orchestator/graph.py`**: Define el flujo completo de la simulación usando LangGraph. Controla la secuencia: pitch → evaluación inicial → rondas de negociación → ofertas → resolución.

- **`src/agents/entrepreneur/nodes.py`**: Implementa las acciones del emprendedor (generar pitch, hacer concesiones, evaluar ofertas).

- **`src/agents/judge/nodes.py`**: Implementa las acciones de los inversionistas (evaluar pitch, actualizar métricas, generar ofertas).

- **`src/agents/common/llm.py`**: Abstracción del cliente Azure OpenAI con método estático `generate()` para prompts de texto.

- **Scoring modules**: Implementan fórmulas cuantitativas para evaluar tracción (`traction_score`), viabilidad económica (`economic_sanity`), riesgo percibido (`perceived_risk`), y potencial de retorno (`perceived_upside`).

## Configuración

### Variables de entorno (.env)

El proyecto requiere las siguientes variables de entorno para conectarse a Azure OpenAI:

```bash
AZURE_API_KEY=your_azure_api_key
AZURE_ENDPOINT=your_azure_endpoint
AZURE_DEPLOYMENT=your_azure_deployment
AZURE_API_VERSION=your_azure_api_version
```

**Descripción de cada variable:**

- **`AZURE_API_KEY`**: Clave de autenticación del recurso Azure OpenAI. Se obtiene desde Azure Portal → Recurso OpenAI → Keys and Endpoint.

- **`AZURE_ENDPOINT`**: URL base del endpoint de Azure OpenAI. Formato: `https://<resource-name>.openai.azure.com/`

- **`AZURE_DEPLOYMENT`**: Nombre del deployment del modelo en Azure. Ejemplo: `gpt-4o-mini`, `gpt-4-turbo`. Este nombre se configura al desplegar un modelo en el recurso de Azure.

- **`AZURE_API_VERSION`**: Versión de la API de Azure OpenAI. Ejemplo: `2024-02-15-preview`, `2023-12-01-preview`. Consultar documentación oficial de Azure para versiones soportadas.

### Configuración del estado inicial

El archivo `initial_state.py` define el escenario de simulación completo:

**Estructura del emprendedor:**
- Información del negocio (`name`, `description`, `target_market`)
- Métricas financieras (`monthly_revenue`, `monthly_burn`, `gross_margin`)
- Ask de inversión (`investment_needed`, `valuation_ask`, `equity_offered`)
- Scores de evaluación (`founder_experience_score`, `tech_moat_score`, `competition_intensity_score`, `regulatory_risk_score`)

**Estructura de jueces:**
- Perfil de inversión (`risk_tolerance`, `return_target`, `scalability_focus`)
- Comportamiento (`negotiation_aggressiveness`, `showmanship_preference`)
- Restricciones (`ticket_min`, `ticket_max`, `sector_preference`)
- Estado dinámico (se actualiza durante la simulación)

**Parámetros de simulación:**
- `round`: Contador de rondas (inicia en 0)
- `max_rounds`: Número máximo de rondas de negociación
- `finished`: Flag de terminación

## Convenciones de código

### Estilo general

- **Nomenclatura**: 
  - Funciones y variables: `snake_case`
  - Clases: `PascalCase`
  - Constantes: `UPPER_CASE`
  - TypedDicts: `PascalCase` con sufijo `State` para estados de agentes

- **Type hints**: Todas las funciones públicas deben incluir anotaciones de tipo completas para parámetros y retornos.

- **Docstrings**: Funciones complejas deben incluir docstrings descriptivos explicando parámetros, retornos y efectos secundarios.

### Estructura de agentes

Cada tipo de agente sigue la estructura:
```
agent_name/
├── nodes.py          # Funciones async que modifican estado
├── state.py          # TypedDict que define el schema del estado
├── prompts.py        # Plantillas de prompts como strings
├── scoring.py        # Funciones de evaluación cuantitativa
└── (otros módulos específicos)
```

### Nodos de LangGraph

Los nodos son funciones async con firma:
```python
async def node_name(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Procesa el estado y retorna un diccionario con actualizaciones.
    Solo las claves retornadas se actualizan en el estado global.
    """
    # Lógica del nodo
    return {"key_to_update": new_value}
```

### Prompts

Los prompts se definen como strings con placeholders de `.format()`:
```python
PROMPT_NAME = """
Eres un {role} que {context}.

Datos:
{data}

Instrucciones:
{instructions}
"""
```

Usar JSON serialization para estructuras complejas en prompts:
```python
prompt = TEMPLATE.format(
    data=json.dumps(complex_dict, ensure_ascii=False)
)
```

### Scoring y matemáticas

- Usar `clamp()` de `src/agents/common/math.py` para normalizar scores en rangos definidos (default: -3 a 3).
- Usar `sigmoid()` para convertir scores continuos a probabilidades [0, 1].
- Las funciones de scoring deben manejar valores `None` y `0` gracefully con operadores ternarios: `value or default_value`.

### Logging de eventos

El sistema mantiene un `event_log` en el estado global. Para agregar eventos:
```python
logs = list(state.get("event_log", []))
logs.append({
    "event": "event_name",
    "timestamp": datetime.utcnow().isoformat(),
    # ... campos específicos del evento
})
return {"event_log": logs}
```

Tipos de eventos estándar:
- `pitch_narrative`: Pitch del emprendedor
- `judge_evaluation`: Evaluación inicial de un juez
- `dialogue_turn`: Turno de conversación
- `offer_made`: Oferta de inversión generada
- `entrepreneur_concession`: Concesión del emprendedor
- `round_summary`: Resumen de ronda por el orquestador

## Roadmap

### Próximas mejoras

**Corto plazo:**
- Implementar suite de tests unitarios e integración (pytest)
- Agregar validación de schemas con Pydantic para `initial_state`
- Implementar logging estructurado con niveles (debug, info, warning)
- Crear CLI con argumentos para parametrizar simulaciones sin modificar código

**Mediano plazo:**
- Persistencia de simulaciones en base de datos (PostgreSQL/MongoDB)
- Dashboard web para visualizar simulaciones en tiempo real
- Exportación de reportes en PDF/HTML con análisis completo
- Soporte para múltiples proveedores de LLM (OpenAI directo, Anthropic Claude)
- Sistema de templates para diferentes escenarios de negociación

**Largo plazo:**
- Análisis estadístico agregado de múltiples simulaciones
- Fine-tuning de modelos en comportamientos de negociación específicos
- Modo multi-jugador donde humanos pueden participar como jueces
- Integración con datos reales de startups (Crunchbase, PitchBook)
- Sistema de recomendaciones para emprendedores basado en patrones históricos

### Funcionalidades en investigación

- Modelado de emociones y psicología de negociación
- Detección de sesgos cognitivos en evaluaciones de jueces
- Simulación de dinámicas de competencia entre jueces
- Incorporación de factores externos (condiciones de mercado, noticias)

## Licencia

Este proyecto no especifica licencia. Para uso comercial o redistribución, contactar a los autores.

## Créditos

**Autor**: Salog0d

**Tecnologías de terceros:**
- LangChain/LangGraph por Harrison Chase y equipo
- Azure OpenAI Service por Microsoft
- FastAPI por Sebastián Ramírez

**Inspiración**: Programas de inversión tipo Shark Tank, Dragon's Den, y literatura sobre negociación algorítmica y sistemas multi-agente.

---

**Nota**: Este proyecto está en fase de desarrollo activo. Contribuciones, issues y pull requests son bienvenidos.
