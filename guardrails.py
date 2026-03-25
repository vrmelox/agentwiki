import json

def clean_and_parse(raw: str) -> dict:
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1]
    
    if raw.endswith("```"):
        raw = raw.split("\n", 1)[0]
    
    raw = raw.strip()

    try :
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"error": "JSON invalide", "raw": {raw}}
    
    return result

def is_repeated_action(action_key: str, seen: set) -> bool:
    return action_key in seen

