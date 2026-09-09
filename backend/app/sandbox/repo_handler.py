import os
import shutil
import subprocess
import zipfile
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("repo_handler")


def clone_repo(source_url: str, submission_id: str) -> str:
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


def extract_zip(zip_path: str, submission_id: str) -> str:
    target_dir = os.path.join(settings.SANDBOX_WORKDIR, str(submission_id))
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    logger.info(f"Extracting {zip_path} into {target_dir}")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(target_dir)
    entries = os.listdir(target_dir)
    if len(entries) == 1 and os.path.isdir(os.path.join(target_dir, entries[0])):
        inner = os.path.join(target_dir, entries[0])
        for item in os.listdir(inner):
            shutil.move(os.path.join(inner, item), target_dir)
        os.rmdir(inner)
    return target_dir


def get_project_source(submission, submission_id: str) -> str:
    if submission.submission_type in ("github", "gitlab"):
        return clone_repo(submission.source_url, submission_id)
    elif submission.submission_type == "zip":
        return extract_zip(submission.source_url, submission_id)
    else:
        raise ValueError(f"Unsupported submission_type for source intake: {submission.submission_type}")


def cleanup_repo(local_path: str):
    if os.path.exists(local_path):
        shutil.rmtree(local_path, ignore_errors=True)
        logger.info(f"Cleaned up {local_path}")
