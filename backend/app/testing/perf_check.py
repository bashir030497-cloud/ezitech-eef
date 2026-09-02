import requests
import time


def run_perf_check(health_endpoint: str) -> dict:
    if not health_endpoint:
        return {"passed": False, "response_time_ms": None, "details": "No endpoint configured"}

    try:
        start = time.time()
        response = requests.get(health_endpoint, timeout=10)
        elapsed_ms = (time.time() - start) * 1000

        return {
            "passed": elapsed_ms < 2000 and response.status_code == 200,
            "response_time_ms": round(elapsed_ms, 2),
        }
    except requests.RequestException as e:
        return {"passed": False, "response_time_ms": None, "details": str(e)}
