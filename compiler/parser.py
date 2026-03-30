# FILE: compiler/parser.py

def parse_katlaz(code: str):
    lines = code.splitlines()
    ast = []

    for line in lines:
        line = line.strip()

        if line.startswith("route"):
            name = line.split(" ")[1].replace(":", "")
            ast.append({"type": "route", "name": name})

        elif line.startswith("print"):
            value = line.replace("print", "").strip()
            ast.append({"type": "print", "value": value})

    return ast
