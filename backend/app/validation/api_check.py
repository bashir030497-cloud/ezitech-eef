import requests


def check_api(health_endpoint: str) -> dict:
    if not health_endpoint:
        return {"reachable": False, "passed": False, "reason": "No health endpoint configured"}

    try:
        response = requests.get(health_endpoint, timeout=10)
        return {
            "reachable": True,
            "status_code": response.status_code,
            "passed": response.status_code == 200,
        }
    except requests.RequestException as e:
        return {"reachable": False, "passed": False, "reason": str(e)}
