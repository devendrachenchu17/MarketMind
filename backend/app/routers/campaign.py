from fastapi import APIRouter, HTTPException, Depends
from app.models.campaign import CampaignRequest, CampaignResponse
from app.services.campaign_service import generate_campaign

router = APIRouter(
    prefix="/api/v1/campaign",
    tags=["Campaign Generator"]
)

@router.post("/generate", response_model=CampaignResponse)
async def create_campaign(request: CampaignRequest):
    """
    Generate a marketing campaign based on product details and target audience.
    """
    try:
        response = await generate_campaign(request)
        if response.campaign_id == "error":
             raise HTTPException(status_code=500, detail=response.strategy_explanation)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
