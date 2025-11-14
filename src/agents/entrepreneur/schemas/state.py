from pydantic import BaseModel, Field
from typing import List, Tuple

class EntrepreneurStateSchema(BaseModel):
    name: str = Field(..., description="Startup name")
    description: str
    target_market: str
    revenue_model: str
    current_traction: str
    investment_needed: str
    use_of_funds: str

    # flujo interno
    negotiations: List[str] = Field(default_factory=list)
    verdict_expanded: Tuple[bool, str] | None = None
    verdict: bool | None = None
