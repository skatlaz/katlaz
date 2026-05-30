# FILE: katlazapp/compiler/transpiler.py
from __future__ import annotations

import ast as py_ast


def transpile(ast):
    lines = [
        "from katlazapp.runtime.core import register_route, emit",
        "from katlazapp.runtime.types import validate_type, cast_type",
        "from katlazapp.runtime.db import insert, select, conn",
        "from katlazapp.runtime.fs import read, write",
        "from katlazapp.runtime.errors import error",
        "from katlazapp.runtime.native import call_python, call_cpp",
        "",
    ]
    for node in ast:
        if node["type"] == "model":
            lines.extend(transpile_model(node))
        elif node["type"] == "route":
            lines.extend(transpile_route(node))
    return "\n".join(lines)


def transpile_model(node):
    name = node["name"]
    fields = []
    for f in node["fields"]:
        typ = {"int": "INTEGER", "bool": "INTEGER", "float": "REAL", "string": "TEXT", "str": "TEXT"}.get(f["type"], "TEXT")
        fields.append(f"{f['name']} {typ}")
    sql = f'CREATE TABLE IF NOT EXISTS {name} ({", ".join(fields)})'
    return [f'conn.execute("""{sql}""")', "conn.commit()", ""]


def transpile_route(node):
    name = node["name"]
    body = []
    for p in node["params"]:
        pname, ptype = p["name"], p["type"]
        body += [
            f"    {pname} = data.get('{pname}')",
            f"    if not validate_type({pname}, '{ptype}'):",
            f"        return error(\"Invalid type for '{pname}'\", hint=\"Expected {ptype}\")",
            f"    {pname} = cast_type({pname}, '{ptype}')",
        ]
    for stmt in node["body"]:
        body.extend(transpile_statement(stmt))
    if not any(line.lstrip().startswith("return ") for line in body):
        body.append("    return {}")
    return [f"def route_{name}(**data):"] + (body or ["    return {}"]) + ["", f'register_route("{name}", route_{name})', ""]


def _literal_or_expr(value: str | None):
    if value is None or value == "":
        return "None"
    return value


def _token_to_py(token: str):
    # shlex removes quotes, so re-quote non numeric words that are not obvious variables.
    if token in {"True", "False", "None"}:
        return token
    try:
        float(token)
        return token
    except ValueError:
        pass
    # allow explicit Python expressions wrapped with ${...}
    if token.startswith("${") and token.endswith("}"):
        return token[2:-1]
    return repr(token)


def _dict_from_pairs(pairs_text: str):
    items = []
    for pair in pairs_text.split(","):
        k, v = pair.split(":", 1)
        items.append(f"{k.strip()!r}: {v.strip()}")
    return "{" + ", ".join(items) + "}"


def transpile_statement(stmt):
    t = stmt["type"]
    if t in {"emit", "view_emit"}:
        data = _literal_or_expr(stmt.get("data"))
        return [f'    return emit("{stmt["event"]}", {data})']
    if t == "return":
        return [f"    return {stmt['expr']}"]
    if t == "assign":
        return [f"    {stmt['var']} = {stmt['expr']}"]
    if t == "py_call":
        args = ", ".join(_token_to_py(a) for a in stmt["args"])
        return [f"    return call_python({stmt['target']!r}{', ' if args else ''}{args})"]
    if t == "cpp_call":
        args = ", ".join(_token_to_py(a) for a in stmt["args"])
        return [f"    return call_cpp({stmt['library']!r}, {stmt['function']!r}{', ' if args else ''}{args})"]
    if t == "db_insert":
        return [f"    insert('{stmt['table']}', {_dict_from_pairs(stmt['data'])})"]
    if t == "db_select":
        return [f"    return select('{stmt['table']}')"]
    if t == "fs_read":
        return [f"    return read('{stmt['path']}')"]
    if t == "fs_write":
        return [f"    write('{stmt['path']}', {stmt['content']!r})"]
    return [f"    {stmt.get('value', 'pass')}"]
