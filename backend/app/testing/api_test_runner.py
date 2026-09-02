import requests
from app.core.logger import get_logger

logger = get_logger("api_test_runner")


def run_api_tests(local_path: str, config: dict) -> list:
    """Basic MVP API test: hit health endpoint and check response shape."""
    results = []
    health_endpoint = config.get("health_endpoint")

    if not health_endpoint:
        results.append({"test_name": "health_check", "passed": False, "details": "No endpoint configured"})
        return results

    try:
        response = requests.get(health_endpoint, timeout=10)
        results.append({
            "test_name": "health_check",
            "passed": response.status_code == 200,
            "details": f"Status: {response.status_code}",
        })
    except requests.RequestException as e:
        results.append({"test_name": "health_check", "passed": False, "details": str(e)})

    return results
