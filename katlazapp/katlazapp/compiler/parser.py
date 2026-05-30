# FILE: katlazapp/compiler/parser.py
from __future__ import annotations

import re
import shlex
from typing import Any


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_params(param_str: str):
    params = []
    for p in param_str.split(","):
        p = p.strip()
        if not p:
            continue
        if ":" in p:
            name, typ = p.split(":", 1)
            params.append({"name": name.strip(), "type": typ.strip()})
        else:
            params.append({"name": p, "type": "any"})
    return params


def parse_katlaz(code: str):
    # Preserve indentation; ignore empty lines/comments.
    raw_lines = []
    for n, line in enumerate(code.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        raw_lines.append((n, line.rstrip()))

    i = 0
    ast = []
    while i < len(raw_lines):
        lineno, line = raw_lines[i]
        stripped = line.strip()

        if stripped.startswith("model "):
            name = stripped.split()[1].replace(":", "")
            base_indent = _indent(line)
            i += 1
            fields = []
            while i < len(raw_lines) and _indent(raw_lines[i][1]) > base_indent:
                f = raw_lines[i][1].strip().split()
                if len(f) < 2:
                    raise SyntaxError(f"[Katlaz Syntax Error] line {raw_lines[i][0]}: field needs name and type")
                fields.append({"name": f[0], "type": f[1]})
                i += 1
            ast.append({"type": "model", "name": name, "fields": fields})
            continue

        if stripped.startswith("route "):
            header = stripped[len("route "):].rstrip(":")
            if "(" in header:
                name, params = header.split("(", 1)
                params = parse_params(params.replace(")", ""))
            else:
                name, params = header, []
            base_indent = _indent(line)
            i += 1
            body = []
            while i < len(raw_lines) and _indent(raw_lines[i][1]) > base_indent:
                body.append(parse_statement(raw_lines[i][1].strip(), raw_lines[i][0]))
                i += 1
            ast.append({"type": "route", "name": name.strip(), "params": params, "body": body})
            continue

        raise SyntaxError(f"[Katlaz Syntax Error] line {lineno}: expected 'model' or 'route'")
    return ast


def _split_command(line: str):
    return shlex.split(line, posix=True)


def parse_statement(line: str, lineno: int):
    try:
        if line.startswith("emit "):
            m = re.match(r'emit\s+"([^"]+)"(?:,\s*(.+))?$', line)
            if not m: raise ValueError("invalid emit syntax")
            return {"type": "emit", "event": m.group(1), "data": m.group(2)}

        if line.startswith("view.emit "):
            m = re.match(r'view\.emit\s+"([^"]+)"(?:,\s*(.+))?$', line)
            if not m: raise ValueError("invalid view.emit syntax")
            return {"type": "view_emit", "event": m.group(1), "data": m.group(2)}

        if line.startswith("py.call "):
            parts = _split_command(line)
            return {"type": "py_call", "target": parts[1], "args": parts[2:]}

        if line.startswith("cpp.call "):
            parts = _split_command(line)
            if len(parts) < 3: raise ValueError("cpp.call needs library and function")
            return {"type": "cpp_call", "library": parts[1], "function": parts[2], "args": parts[3:]}

        if line.startswith("return "):
            return {"type": "return", "expr": line[len("return "):].strip()}

        if line.startswith("db.insert"):
            m = re.match(r'db\.insert\s+"([^"]+)",\s*\{(.+)\}', line)
            if not m: raise ValueError("invalid db.insert syntax")
            return {"type": "db_insert", "table": m.group(1), "data": m.group(2)}

        if line.startswith("db.select"):
            m = re.match(r'db\.select\s+"([^"]+)"', line)
            if not m: raise ValueError("invalid db.select syntax")
            return {"type": "db_select", "table": m.group(1)}

        if line.startswith("fs.read"):
            m = re.match(r'fs\.read\s+"([^"]+)"', line)
            if not m: raise ValueError("invalid fs.read syntax")
            return {"type": "fs_read", "path": m.group(1)}

        if line.startswith("fs.write"):
            m = re.match(r'fs\.write\s+"([^"]+)",\s*"([^"]+)"', line)
            if not m: raise ValueError("invalid fs.write syntax")
            return {"type": "fs_write", "path": m.group(1), "content": m.group(2)}

        if "=" in line:
            var, expr = line.split("=", 1)
            return {"type": "assign", "var": var.strip(), "expr": expr.strip()}

        return {"type": "raw", "value": line}
    except Exception as exc:
        raise SyntaxError(f"[Katlaz Syntax Error] line {lineno}: {line} ({exc})")
