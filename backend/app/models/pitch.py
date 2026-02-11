from pydantic import BaseModel, Field
from typing import List, Optional

class PitchRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product")
    product_description: str = Field(..., description="Details about the product")
    persona: str = Field(..., description="Target persona (e.g., CTO, Marketing Manager)")
    industry: str = Field(..., description="Industry of the target")
    tone: str = Field("Professional", description="Tone of the pitch")

class PitchVariant(BaseModel):
    variant_type: str = Field(..., description="Type of pitch (e.g., Email, LinkedIn Message, Elevator Pitch)")
    subject_line: Optional[str] = Field(None, description="Subject line for emails")
    content: str = Field(..., description="The pitch content")
    xai_explanation: str = Field(..., description="Why this structure/tone was chosen")

class PitchResponse(BaseModel):
    pitch_id: str
    variants: List[PitchVariant]
    strategy_explanation: str = Field(..., description="Overall persuasion strategy")
