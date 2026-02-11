from fastapi import APIRouter, HTTPException
from app.models.lead import LeadRequest, LeadScoreResponse
from app.services.lead_service import score_lead

router = APIRouter(
    prefix="/api/v1/lead",
    tags=["Lead Scoring"]
)

@router.post("/score", response_model=LeadScoreResponse)
async def analyze_lead(request: LeadRequest):
    try:
        response = await score_lead(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
