import os


def run_db_tests(local_path: str) -> dict:
    """MVP check: confirm migration/schema files exist and are non-empty."""
    found_valid = False
    for root, dirs, files in os.walk(local_path):
        for file in files:
            if "migration" in file.lower() or file.endswith(".sql"):
                path = os.path.join(root, file)
                if os.path.getsize(path) > 0:
                    found_valid = True

    return {"passed": found_valid, "details": "Migration/schema files checked"}
