# FILE: katlazapp/runtime/bridge.py

import json
from katlazapp.runtime.core import call_route


def handle(payload: str):
    try:
        data = json.loads(payload)
    except Exception:
        return {"error": "Invalid JSON"}

    if not isinstance(data, dict):
        return {"error": "Payload must be object"}

    name = data.get("name")
    args = data.get("data") or {}

    if not name:
        return {"error": "Missing route name"}

    return call_route(name, args)
