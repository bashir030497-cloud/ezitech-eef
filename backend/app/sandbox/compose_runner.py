import re
import subprocess
from app.core.logger import get_logger

logger = get_logger("compose_runner")


def _strip_fixed_host_ports(local_path: str) -> None:
    for name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"):
        path = f"{local_path}/{name}"
        try:
            with open(path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            continue

        new_content = re.sub(
            r'-\s*(["\']?)(\d{2,5}):(\d{2,5})(["\']?)',
            lambda m: f'- {m.group(1)}{m.group(3)}{m.group(1)}',
            content,
        )

        if new_content != content:
            with open(path, "w") as f:
                f.write(new_content)
            logger.info(f"Rewrote fixed host ports to dynamic ports in {name}")
        break


def compose_up(local_path: str, project_name: str, timeout: int = 600) -> None:
    _strip_fixed_host_ports(local_path)
    logger.info(f"Starting docker-compose stack for {project_name}")
    result = subprocess.run(
        ["docker-compose", "-p", project_name, "up", "-d", "--build"],
        cwd=local_path,
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        logger.error(f"docker-compose up failed: {result.stderr}")
        raise RuntimeError(f"docker-compose up failed: {result.stderr}")


def compose_down(local_path: str, project_name: str) -> None:
    try:
        subprocess.run(
            ["docker-compose", "-p", project_name, "down", "-v", "--remove-orphans"],
            cwd=local_path,
            capture_output=True, text=True, timeout=60,
        )
        logger.info(f"Tore down docker-compose stack for {project_name}")
    except Exception as e:
        logger.error(f"docker-compose down failed (non-fatal): {e}")


def compose_service_port(local_path: str, project_name: str, service: str, internal_port: int):
    result = subprocess.run(
        ["docker-compose", "-p", project_name, "port", service, str(internal_port)],
        cwd=local_path,
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout.strip().split(":")[-1]
