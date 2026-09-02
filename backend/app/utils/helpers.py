import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def safe_get(dictionary: dict, key: str, default=None):
    return dictionary.get(key, default)


def truncate_text(text: str, max_length: int = 500) -> str:
    if text and len(text) > max_length:
        return text[:max_length] + "..."
    return text
