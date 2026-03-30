# FILE: katlazapp/compiler/parser.py
import re


def parse_params(param_str):
    params = []

    for p in param_str.split(","):
        p = p.strip()
        if not p:
            continue

        if ":" in p:
            name, typ = p.split(":")
            params.append({
                "name": name.strip(),
                "type": typ.strip()
            })
        else:
            params.append({
                "name": p,
                "type": "any"
            })

    return params


def parse_katlaz(code: str):
    lines = [l.rstrip() for l in code.splitlines() if l.strip()]
    i = 0
    ast = []

    while i < len(lines):
        line = lines[i]

        # MODEL
        if line.startswith("model "):
            name = line.split()[1].replace(":", "")
            i += 1

            fields = []

            while i < len(lines) and lines[i].startswith("    "):
                f = lines[i].strip().split()
                fields.append({"name": f[0], "type": f[1]})
                i += 1

            ast.append({
                "type": "model",
                "name": name,
                "fields": fields
            })
            continue

        # ROUTE
        if line.startswith("route "):
            header = line.replace("route ", "").replace(":", "")

            if "(" in header:
                name, params = header.split("(")
                params = parse_params(params.replace(")", ""))
            else:
                name = header
                params = []

            i += 1
            body = []

            while i < len(lines) and lines[i].startswith("    "):
                body.append(parse_statement(lines[i].strip(), i+1))
                i += 1

            ast.append({
                "type": "route",
                "name": name,
                "params": params,
                "body": body
            })
            continue

        i += 1

    return ast


def parse_statement(line, lineno):
    try:
        if line.startswith("emit "):
            m = re.match(r'emit\s+"([^"]+)"(?:,\s*(.+))?', line)
            return {"type": "emit", "event": m.group(1), "data": m.group(2)}

        if line.startswith("db.insert"):
            m = re.match(r'db\.insert\s+"([^"]+)",\s*\{(.+)\}', line)
            return {"type": "db_insert", "table": m.group(1), "data": m.group(2)}

        if line.startswith("db.select"):
            m = re.match(r'db\.select\s+"([^"]+)"', line)
            return {"type": "db_select", "table": m.group(1)}

        if line.startswith("fs.read"):
            m = re.match(r'fs\.read\s+"([^"]+)"', line)
            return {"type": "fs_read", "path": m.group(1)}

        if line.startswith("fs.write"):
            m = re.match(r'fs\.write\s+"([^"]+)",\s*"([^"]+)"', line)
            return {
                "type": "fs_write",
                "path": m.group(1),
                "content": m.group(2)
            }

        if "=" in line:
            var, expr = line.split("=", 1)
            return {"type": "assign", "var": var.strip(), "expr": expr.strip()}

        return {"type": "raw", "value": line}

    except Exception:
        raise Exception(f"[Katlaz Syntax Error] line {lineno}: {line}")

