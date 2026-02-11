import json
from app.models.pitch import PitchRequest, PitchResponse, PitchVariant
from app.utils.llm_client import llm_client

async def generate_pitch(request: PitchRequest) -> PitchResponse:
    # Check for mock mode first (if API key is missing, LLMClient handles it, but we need specific mock data for Pitch)
    if not llm_client.api_key:
         return PitchResponse(
            pitch_id="mock_pitch_123",
            strategy_explanation="DEMO MODE: Strategy focused on value-based selling and addressing pain points specific to the persona.",
            variants=[
                PitchVariant(
                    variant_type="Cold Email",
                    subject_line=f"Unlock growth for {request.industry} with {request.product_name}",
                    content=f"Hi [Name],\n\nI noticed you're leading innovation in the {request.industry} space. {request.product_name} helps teams like yours streamline operations.\n\nWould you be open to a 10-min chat?",
                    xai_explanation="Short, direct approach respecting the recipient's time. value proposition is front-loaded."
                ),
                PitchVariant(
                    variant_type="LinkedIn Message",
                    content=f"Saw your recent post about {request.industry} trends. {request.product_name} aligns perfectly with that vision. Let's connect!",
                    xai_explanation="Contextual and personalized to recent activity to increase acceptance rate."
                ),
                PitchVariant(
                    variant_type="Elevator Pitch",
                    content=f"{request.product_name} is the only solution that combines X and Y for {request.persona}s, reducing costs by 20% in just 30 days.",
                    xai_explanation="Focuses on unique selling proposition (USP) and quantifiable metrics."
                )
            ]
        )

    system_prompt = """
    You are an expert Sales Copywriter and Deal Closer.
    Generate personalized sales pitches based on the product and target persona.
    Provide Explainable AI (XAI) reasoning for your choices.
    
    CRITICAL: You MUST respond with a VALID JSON object.
    Example format:
    {
        "strategy_explanation": "...",
        "variants": [
            {
                "variant_type": "Cold Email",
                "subject_line": "...",
                "content": "Full email text",
                "xai_explanation": "..."
            }
        ]
    }
    """
    
    user_prompt = f"""
    Product: {request.product_name}
    Description: {request.product_description}
    Persona: {request.persona}
    Industry: {request.industry}
    Tone: {request.tone}
    
    Generate 3 distinct variants: 'Cold Email', 'LinkedIn Message', and 'Elevator Pitch'.
    Ensure 'content' is detailed and ready to use.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response_text = await llm_client.generate(messages)
    print(f"DEBUG: Pitch AI raw response: {response_text[:300]}")
    
    try:
        # Clean JSON if AI adds markdown
        clean_json = response_text
        if "```json" in response_text:
            clean_json = response_text.split("```json")[1].split("```")[0].strip()
        elif "{" in response_text:
            clean_json = response_text[response_text.find("{"):response_text.rfind("}")+1]

        data = json.loads(clean_json)
        variants = []
        for item in data.get("variants", []):
            variants.append(PitchVariant(
                variant_type=item.get("variant_type", "Unknown"),
                subject_line=item.get("subject_line"),
                content=item.get("content", "No content generated"),
                xai_explanation=item.get("xai_explanation", "")
            ))
            
        # Use abs() and modulo to avoid indexing issues and signs
        res_id = f"gen_pitch_{abs(hash(clean_json)) % 1000000}"
        
        return PitchResponse(
            pitch_id=res_id,
            variants=variants,
            strategy_explanation=data.get("strategy_explanation", "Generated based on sales best practices.")
        )

    except Exception as e:
        print(f"ERROR: Pitch parsing failed: {e}")
        return PitchResponse(
            pitch_id="error",
            variants=[],
            strategy_explanation=f"Error parsing AI response: {str(e)}"
        )

