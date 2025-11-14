from pydantic import BaseModel
from typing import List, Dict, Any
from enum import Enum
from src.agents.entrepreneur.graph.state import EntrepreneurState
from src.agents.judge.graph.state import JudgeState

class PHASES(str, Enum):
    proposal   = "proposal"
    analysis   = "analysis"
    offer      = "offer"
    resolution = "resolution"


class OrchestratorState(BaseModel):

    entrepreneur: EntrepreneurState
    judges: List[JudgeState]

    # Full timeline of events
    rounds_history: List[Dict[str, Any]] = []

    # Global phase tracker
    phase: PHASES = PHASES.proposal

    # Metrics computed during simulation
    market_context: Dict[str, Any] = {}           # external APIs / tools
    judge_consensus_score: float | None = None
    deal_quality_score: float | None = None
    fairness_score: float | None = None
    negotiation_efficiency_score: float | None = None

    # Iteration control
    round: int = 0
    max_rounds: int = 6
    finished: bool = False

    # Debug/logging
    event_log: List[Dict[str, Any]] = []
    random_seed: int | None = None
