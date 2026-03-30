# FILE: runtime/core.py

import json

class KatlazRuntime:
    def __init__(self):
        self.routes = {}

    def register(self, name, func):
        self.routes[name] = func

    def handle(self, payload):
        data = json.loads(payload)
        name = data.get("name")
        args = data.get("data", {})

        if name in self.routes:
            return self.routes[name](args)

        return {"error": f"Route '{name}' not found"}
