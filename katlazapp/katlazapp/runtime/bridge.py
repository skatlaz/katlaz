# FILE: katlazapp/runtime/bridge.py
from __future__ import annotations

import json
from typing import Any

from katlazapp.runtime.core import call_route
from katlazapp.runtime.errors import error


def handle(payload: str | bytes | dict[str, Any]):
    """Bridge universal: WebView JS, HTTP API and native windows call this.

    Input accepted:
        {"name":"route", "data":{...}}
        {"route":"route", "payload":{...}}
    Output is always JSON-serializable dict.
    """
    try:
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8", errors="replace")
        data = json.loads(payload) if isinstance(payload, str) else payload
    except Exception as exc:
        return error("Invalid JSON", detail=str(exc), code="BRIDGE_JSON_ERROR")

    if not isinstance(data, dict):
        return error("Payload must be object", code="BRIDGE_PAYLOAD_ERROR")

    name = data.get("name") or data.get("route")
    args = data.get("data", data.get("payload", {})) or {}

    if not name:
        return error("Missing route name", code="BRIDGE_ROUTE_MISSING")

    return call_route(str(name), args)


def handle_json(payload: str | bytes | dict[str, Any]) -> str:
    return json.dumps(handle(payload), ensure_ascii=False)
