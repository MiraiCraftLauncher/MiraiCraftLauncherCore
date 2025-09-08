import json

def get_jtoken(content:str) -> dict:
    return json.loads(content)

def to_jstring(content:dict) -> str:
    return json.dumps(content)