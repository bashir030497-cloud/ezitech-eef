import os
import difflib
from sqlalchemy.orm import Session
from app.models.submission import Submission


def _read_all_code(local_path: str) -> str:
    content = ""
    for root, dirs, files in os.walk(local_path):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith((".py", ".js", ".php", ".dart")):
                try:
                    with open(os.path.join(root, file), "r", errors="ignore") as f:
                        content += f.read()
                except Exception:
                    continue
    return content


def check_plagiarism(local_path: str, db: Session, threshold: float = 0.85) -> dict:
    current_code = _read_all_code(local_path)
    matches = []

    # Compare against previously stored submission source paths would require
    # storing code snapshots; for MVP we compare against nothing stored yet.
    # Placeholder for future: fetch stored code hashes/snippets from DB.

    similarity_score = 0.0
    return {
        "score": f"{similarity_score * 100:.0f}%",
        "matches": ",".join(matches) if matches else "none",
    }
