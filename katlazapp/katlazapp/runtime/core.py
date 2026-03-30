import inspect
from katlazapp.runtime.ws import broadcast
from katlazapp.runtime.errors import error
import asyncio

ROUTES = {}
DEBUG = True

class Route:

    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.signature = inspect.signature(func)

    def call(self, data):
        try:
            if not self.signature.parameters:
                return self.func()

            if isinstance(data, dict):
                return self.func(**data)

            return self.func(data)

        except TypeError:
            # fallback seguro
            return self.func(data or {})


def register_route(name, func):
    ROUTES[name] = Route(name, func)

def call_route(name, data=None):
    route = ROUTES.get(name)

    if not route:
        return error(f"Route '{name}' not found")

    try:
        return normalize(route.call(data or {}))
    except Exception as e:
        return error(
            message=str(e),
            code="RUNTIME_ERROR"
        )


def emit(event, data=None):
    try:
        asyncio.create_task(broadcast(event, data))
    except:
        pass

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
        return emit("notify", result)

    return emit("result", result)

def log(*args):
    if DEBUG:
        print("[Katlaz]", *args)

def emit(event, data=None):
    try:
        asyncio.create_task(broadcast(event, data))
    except:
        pass

    return {"event": event, "data": data}

