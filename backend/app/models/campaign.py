from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CampaignRequest(BaseModel):
    product_name: str = Field(..., description="Name of the product or service")
    product_description: str = Field(..., description="Detailed description of the product")
    target_audience: str = Field(..., description="Description of the target audience")
    platforms: List[str] = Field(..., description="List of platforms to generate content for (e.g., LinkedIn, Twitter, Instagram)")
    tone: str = Field("Professional", description="Desired tone of the campaign")

class ContentItem(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    visual_prompt: str = Field(..., description="Prompt for generating visuals")
    media_url: Optional[str] = Field(None, description="URL of generated media (if available)")
    xai_explanation: str = Field(..., description="Explainable AI: Why this content/tone/visual was chosen")

class CampaignResponse(BaseModel):
    campaign_id: str
    generated_content: List[ContentItem]
    strategy_explanation: str = Field(..., description="Overall strategy explanation")
