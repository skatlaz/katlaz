import json

clients = set()


async def ws_handler(ws):
    clients.add(ws)

    try:
        async for msg in ws:
            data = json.loads(msg)

            from katlazapp.runtime.core import call_route

            res = call_route(
                data.get("name"),
                data.get("data") or {}
            )

            await ws.send(json.dumps(res))

    finally:
        clients.remove(ws)


# =============================
# BROADCAST GLOBAL
# =============================
async def broadcast(event, data):
    payload = json.dumps({
        "event": event,
        "data": data
    })

    for ws in clients:
        await ws.send(payload)
