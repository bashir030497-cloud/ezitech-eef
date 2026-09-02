import yaml
import os

CONFIG_DIR = os.path.dirname(__file__)


def get_language_config(language_stack: str) -> dict:
    file_path = os.path.join(CONFIG_DIR, f"{language_stack}.yaml")
    if not os.path.exists(file_path):
        raise ValueError(f"No sandbox config found for: {language_stack}")
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
