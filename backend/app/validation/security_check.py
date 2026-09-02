import os
import re

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",              # AWS key
    r"AIza[0-9A-Za-z\-_]{35}",        # Google API key
    r"(?i)api[_-]?key\s*=\s*['\"][^'\"]+['\"]",
    r"(?i)secret\s*=\s*['\"][^'\"]+['\"]",
    r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
]


def check_security(local_path: str) -> dict:
    issues = []
    for root, dirs, files in os.walk(local_path):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith((".py", ".js", ".env", ".php", ".yaml", ".yml")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", errors="ignore") as f:
                        content = f.read()
                        for pattern in SECRET_PATTERNS:
                            if re.search(pattern, content):
                                issues.append(f"Possible hardcoded secret in {file}")
                except Exception:
                    continue

    return {
        "issues_found": issues,
        "passed": len(issues) == 0,
    }
