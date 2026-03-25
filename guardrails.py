import json

def clean_and_parse(raw: str) -> dict:
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    lines = raw.split("\n")
    if lines[-1].strip() == "```":
        lines = lines[:-1]
    raw = "\n".join(lines)
    
    raw = raw.strip()

    try :
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"error": "JSON invalide", "raw": raw}
    
    return result

def is_repeated_action(action_key: str, seen: set) -> bool:
    return action_key in seen


def truncate(text: str, max_chars: int = 800) -> str:
    if len(text) > max_chars :
        return f"{text[:800]} + [tronqué - {len(text) - max_chars}]"
    return text