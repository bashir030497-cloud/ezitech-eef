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
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "You return only valid JSON, no markdown, no explanation."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 1000,
                "temperature": 0.3,
            },
            timeout=30,
        )
        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"].get("message", "Unknown OpenAI error"))

        text = data["choices"][0]["message"]["content"]
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
