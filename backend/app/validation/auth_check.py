import requests


def check_auth(auth_endpoint: str) -> dict:
    if not auth_endpoint:
        return {"checked": False, "passed": False, "reason": "No auth endpoint configured"}

    try:
        response = requests.post(auth_endpoint, json={"email": "test@test.com", "password": "wrong"}, timeout=10)
        return {
            "checked": True,
            "status_code": response.status_code,
            "passed": response.status_code in [200, 401, 422],
        }
    except requests.RequestException as e:
        return {"checked": False, "passed": False, "reason": str(e)}
