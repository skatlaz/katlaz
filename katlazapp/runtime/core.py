# FILE: katlazapp/runtime/core.py

ROUTES = {}

def register_route(name, func):
    ROUTES[name] = func


def call_route(name, data=None):
    if name not in ROUTES:
        return {"error": f"Route '{name}' not found"}

    try:
        result = ROUTES[name](data or {})
    except Exception as e:
        return {"error": str(e)}

    return normalize(result)


def emit(event, data=None):
    return {
        "event": event,
        "data": data
    }


def normalize(result):
    if result is None:
        return {}

    if isinstance(result, dict):
        return result

    if isinstance(result, str):
        return {"event": "notify", "data": result}

    return {"event": "result", "data": result}
