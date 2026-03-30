# FILE: katlazapp/runtime/bridge.py

import json
from katlazapp.runtime.core import call_route


def handle(payload: str):
    try:
        data = json.loads(payload)
    except Exception:
        return {"error": "Invalid JSON"}

    name = data.get("name")
    args = data.get("data", {})

    if not name:
        return {"error": "Missing route name"}

    return call_route(name, args)
