from __future__ import annotations

import asyncio
import inspect
from katlazapp.runtime.errors import error
from katlazapp.runtime.ws import broadcast

ROUTES = {}
DEBUG = True


class Route:
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.signature = inspect.signature(func)

    def call(self, data):
        if not self.signature.parameters:
            return self.func()
        if isinstance(data, dict):
            return self.func(**data)
        return self.func(data)


def register_route(name, func):
    ROUTES[str(name)] = Route(str(name), func)


def call_route(name, data=None):
    route = ROUTES.get(str(name))
    if not route:
        return error(f"Route '{name}' not found", code="ROUTE_NOT_FOUND")
    try:
        return normalize(route.call(data or {}))
    except TypeError:
        try:
            return normalize(route.func(data or {}))
        except Exception as exc:
            return error(str(exc), code="RUNTIME_ERROR")
    except Exception as exc:
        return error(str(exc), code="RUNTIME_ERROR")


def emit(event, data=None):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(broadcast(event, data))
    except Exception:
        pass
    return {"event": event, "data": data}


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
