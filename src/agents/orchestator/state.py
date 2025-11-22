from typing import TypedDict, List, Dict, Any
from src.agents.entrepreneur.state import EntrepreneurState
from src.agents.judge.state import JudgeState


class OrchestratorState(TypedDict, total=False):
    entrepreneur: EntrepreneurState
    judges: List[JudgeState]

    phase: str

    rounds_history: List[Dict[str, Any]]
    event_log: List[Dict[str, Any]]
    market_context: Dict[str, Any]

    round: int
    max_rounds: int
    finished: bool
