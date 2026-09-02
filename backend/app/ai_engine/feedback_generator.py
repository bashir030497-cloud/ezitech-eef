import json
import requests
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("feedback_generator")


def generate_feedback(validation_data: dict, test_results: list, scores: dict) -> dict:
    prompt = f"""
You are an engineering evaluator. Based on this data, return ONLY a JSON object with these keys:
strengths, weaknesses, missing_requirements, security_risks, performance_suggestions,
refactoring_suggestions, improvement_roadmap. Each value should be a short string.

Validation data: {json.dumps(validation_data)}
Test results: {json.dumps(test_results)}
Scores: {json.dumps(scores)}
"""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.LLM_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        data = response.json()
        text = data["content"][0]["text"]
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)

    except Exception as e:
        logger.error(f"Feedback generation failed: {e}")
        return {
            "strengths": "N/A",
            "weaknesses": "N/A",
            "missing_requirements": "N/A",
            "security_risks": "N/A",
            "performance_suggestions": "N/A",
            "refactoring_suggestions": "N/A",
            "improvement_roadmap": "Feedback generation failed",
        }
