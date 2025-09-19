import json

def get_jtoken(content:str) -> dict:
    if not content:
        return {}
    return json.loads(content)

def to_jstring(content:dict) -> str:
    if not content:
        content = {}
    return json.dumps(content)