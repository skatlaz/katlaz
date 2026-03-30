import json

def handle(payload):
    data = json.loads(payload)

    name = data["name"]

    if name == "hello":
        print("Python recebeu:", data["data"])
