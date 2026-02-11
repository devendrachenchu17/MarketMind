import os
import httpx
import json
import asyncio
from typing import List, Dict, Any
from app.models.campaign import CampaignRequest, CampaignResponse, ContentItem
from app.utils.llm_client import llm_client

async def generate_campaign(request: CampaignRequest) -> CampaignResponse:
    print(f"Received campaign request for: {request.product_name}")
    
    # Construct the prompt for the LLM
    platforms_str = ", ".join(request.platforms)
    
    system_prompt = """
    You are an expert Marketing Strategist and AI Content Generator for the MarketMind platform.
    Your goal is to generate high-quality, platform-specific marketing content and provide Explainable AI (XAI) reasoning for your choices.
    
    You must output strictly in JSON format matching the following structure:
    {
        "strategy_explanation": "Overall strategy...",
        "generated_content": [
            {
                "platform": "Platform Name",
                "content": "The post content...",
                "hashtags": ["#tag1", "#tag2"],
                "visual_prompt": "Description for an image generator. CRITICAL: Always include the specific product name and its key visual features here.",
                "xai_explanation": "Why this specific content and tone were chosen for this platform..."
            }
        ]
    }
    """
    
    user_prompt = f"""
    Product: {request.product_name}
    Description: {request.product_description}
    Target Audience: {request.target_audience}
    Tone: {request.tone}
    Platforms: {platforms_str}
    
    Platform-Specific Guidelines:
    - Instagram: Focus on high-aesthetic visual storytelling. Captions should be engaging, professional, and invite interaction. Use line breaks for readability.
    - Poster: Concepts for a vertical (9:16) or A3 print poster. Focus on a strong headline, minimal text, and striking visual key art.
    - LinkedIn: Professional, industry-insight driven, value-first.
    
    For 'visual_prompt':
    - For Posters, describe the layout, typography style, and key art.
    - For Social, describe a highly aesthetic, premium image OR a short video concept (e.g., "Video: Time-lapse of...") that would perform well.
    For 'xai_explanation', be specific about why the copy length, emoji usage, and call-to-action were selected for that specific platform and audience.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    print(f"Calling LLM for {request.product_name}...")
    try:
        llm_response = await llm_client.generate(messages)
    except Exception as e:
        print(f"LLM Call Failed: {e}")
        raise e
        
    print("LLM Response received. Parsing JSON...")
    
    try:
        content_dict = json.loads(llm_response)
        print("JSON Parsed successfully.")
        
        tasks = []
        items_to_process = []
        
        generated_content_list = content_dict.get("generated_content", [])
        if not isinstance(generated_content_list, list):
            generated_content_list = []

        for item in generated_content_list:
            visual_prompt = item.get("visual_prompt", "")
            platform = item.get("platform", "").lower()
            
            aspect_ratio = "1:1"
            is_video = False
            
            if "instagram" in platform or "poster" in platform:
                aspect_ratio = "9:16"
            
            if "video" in visual_prompt.lower() or "reel" in platform or "tiktok" in platform:
                is_video = True

            items_to_process.append((item, is_video))
            
            if visual_prompt:
                if is_video:
                    tasks.append(llm_client.generate_video(visual_prompt, aspect_ratio))
                else:
                    tasks.append(llm_client.generate_image(visual_prompt, aspect_ratio))
            else:
                 async def no_op(): return None
                 tasks.append(no_op())
        
        if tasks:
            print(f"DEBUG: Starting parallel generation for {len(tasks)} items...")
            
            async def run_safe(task_coro, idx):
                try:
                    res = await task_coro
                    print(f"DEBUG: Media Item {idx} success: {res[:50] if res else 'None'}...")
                    return res
                except Exception as e:
                    print(f"DEBUG: Media Item {idx} failed: {e}")
                    return None

            wrapped_tasks = [run_safe(t, i) for i, t in enumerate(tasks)]
            
            try:
                results = await asyncio.wait_for(asyncio.gather(*wrapped_tasks), timeout=45.0)
                for (item_dict, _), result in zip(items_to_process, results):
                    item_dict["media_url"] = result
                    print(f"DEBUG: Assigned media_url: {result}")
            except asyncio.TimeoutError:
                print("CRITICAL: Media generation timed out after 45s.")
            except Exception as e:
                print(f"CRITICAL: Unexpected error in parallel generation: {e}")

        content_items = []
        for item_dict in generated_content_list:
            content_items.append(ContentItem(
                platform=item_dict.get("platform", "Unknown"),
                content=item_dict.get("content", ""),
                hashtags=item_dict.get("hashtags", []),
                visual_prompt=item_dict.get("visual_prompt", ""),
                xai_explanation=item_dict.get("xai_explanation", ""),
                media_url=item_dict.get("media_url", None)
            ))
            
        return CampaignResponse(
            campaign_id="gen_" + os.urandom(4).hex(),
            generated_content=content_items,
            strategy_explanation=content_dict.get("strategy_explanation", "Strategy generated based on best practices.")
        )
        
    except json.JSONDecodeError:
        return CampaignResponse(
            campaign_id="error",
            generated_content=[],
            strategy_explanation="Error parsing AI response. Please try again."
        )
