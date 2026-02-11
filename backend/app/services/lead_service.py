import json
from app.models.lead import LeadRequest, LeadScoreResponse
from app.utils.llm_client import llm_client

async def score_lead(request: LeadRequest) -> LeadScoreResponse:
    # Check for mock mode
    if not llm_client.api_key:
        # Simple heuristic for mock
        base_score = 50
        if "High" in request.urgency: base_score += 20
        if "$" in request.budget and len(request.budget) > 4: base_score += 15
        
        priority = "Medium"
        if base_score > 80: priority = "High"
        elif base_score < 40: priority = "Low"
        
        return LeadScoreResponse(
            lead_id="mock_lead_789",
            score=base_score,
            priority=priority,
            conversion_probability=f"{base_score}%",
            qualification_summary=f"Lead shows {request.urgency.lower()} urgency with defined budget.",
            recommended_actions=["Schedule Discovery Call", "Send Case Studies"],
            xai_explanation=f"Score boosted by '{request.urgency}' urgency. Budget presence indicates intent."
        )

    system_prompt = """
    You are an AI Sales Operations Specialist.
    Analyze the lead details and provide a lead score (0-100), priority, and qualification summary.
    Use Explainable AI to justify the score based on BANT (Budget, Authority, Need, Timing).
    
    CRITICAL: You MUST respond with a VALID JSON object.
    Example format:
    {
        "score": 85,
        "priority": "High",
        "conversion_probability": "75%",
        "qualification_summary": "...",
        "recommended_actions": ["...", "..."],
        "xai_explanation": "..."
    }
    """
    
    user_prompt = f"""
    Lead: {request.name} ({request.company})
    Budget: {request.budget}
    Urgency: {request.urgency}
    Needs: {request.needs}
    Notes: {request.notes}
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response_text = await llm_client.generate(messages)
    
    try:
        # Clean JSON if AI adds markdown
        clean_json = response_text
        if "```json" in response_text:
            clean_json = response_text.split("```json")[1].split("```")[0].strip()
        elif "{" in response_text:
            clean_json = response_text[response_text.find("{"):response_text.rfind("}")+1]

        data = json.loads(clean_json)
        # Use abs() and modulo to avoid indexing issues and signs
        res_id = f"gen_lead_{abs(hash(clean_json)) % 1000000}"
        
        return LeadScoreResponse(
            lead_id=res_id,
            score=data.get("score", 50),
            priority=data.get("priority", "Medium"),
            conversion_probability=data.get("conversion_probability", "50%"),
            qualification_summary=data.get("qualification_summary", "Analysis complete."),
            recommended_actions=data.get("recommended_actions", ["Contact Lead"]),
            xai_explanation=data.get("xai_explanation", "Score based on available data.")
        )
    except Exception as e:
        print(f"ERROR: Lead parsing failed: {e}")
        return LeadScoreResponse(
            lead_id="error",
            score=0,
            priority="Unknown",
            conversion_probability="0%",
            qualification_summary=f"Error parsing AI response: {str(e)}",
            recommended_actions=[],
            xai_explanation="Error in AI processing."
        )

