from fastapi import APIRouter, HTTPException
from app.models.pitch import PitchRequest, PitchResponse
from app.services.pitch_service import generate_pitch

router = APIRouter(
    prefix="/api/v1/pitch",
    tags=["Sales Pitch Generator"]
)

@router.post("/generate", response_model=PitchResponse)
async def create_pitch(request: PitchRequest):
    try:
        response = await generate_pitch(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
