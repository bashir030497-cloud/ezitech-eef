import os
import shutil
import subprocess
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("repo_handler")


def clone_repo(source_url: str, submission_id: str) -> str:
    """Clones a GitHub/GitLab repo into a temp workdir. Returns local path."""
    target_dir = os.path.join(settings.SANDBOX_WORKDIR, str(submission_id))

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)

    logger.info(f"Cloning {source_url} into {target_dir}")
    result = subprocess.run(
        ["git", "clone", "--depth", "1", source_url, target_dir],
        capture_output=True, text=True, timeout=120,
    )

    if result.returncode != 0:
        logger.error(f"Clone failed: {result.stderr}")
        raise RuntimeError(f"Clone failed: {result.stderr}")

    return target_dir


def cleanup_repo(local_path: str):
    if os.path.exists(local_path):
        shutil.rmtree(local_path, ignore_errors=True)
        logger.info(f"Cleaned up {local_path}")
