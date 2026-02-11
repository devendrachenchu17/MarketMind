from pydantic import BaseModel, Field
from typing import List, Optional

class LeadRequest(BaseModel):
    name: str = Field(..., description="Lead Name")
    company: str = Field(..., description="Company Name")
    budget: str = Field(..., description="Budget range or amount")
    urgency: str = Field("Medium", description="Urgency level (Low/Medium/High)")
    needs: str = Field(..., description="Specific business needs")
    notes: Optional[str] = Field(None, description="Additional context")

class LeadScoreResponse(BaseModel):
    lead_id: str
    score: int = Field(..., description="Lead Score (0-100)")
    priority: str = Field(..., description="Priority (Low/Medium/High)")
    conversion_probability: str = Field(..., description="Estimated probability (e.g. 'High (75%)')")
    qualification_summary: str = Field(..., description="Summary of qualification")
    recommended_actions: List[str] = Field(..., description="Next steps")
    xai_explanation: str = Field(..., description="Why this score was assigned")
