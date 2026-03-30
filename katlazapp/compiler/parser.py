# FILE: katlazapp/compiler/parser.py

def parse_katlaz(code: str):
    lines = code.splitlines()
    ast = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("route"):
            name = line.split(" ")[1].replace(":", "")
            ast.append({"type": "route", "name": name})

        elif line.startswith("print"):
            value = line.replace("print", "").strip()
            ast.append({"type": "print", "value": value})

        elif line.startswith("emit"):
            parts = line.replace("emit", "").strip().split(",", 1)

            event = parts[0].strip()
            data = parts[1].strip() if len(parts) > 1 else '""'

            ast.append({
                "type": "emit",
                "event": event,
                "data": data
            })

    return ast
