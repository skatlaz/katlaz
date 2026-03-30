# FILE: katlazapp/compiler/transpiler.py

"""
Katlaz Transpiler
-----------------
Converte AST Katlaz → Python executável
"""

from katlazapp.runtime.core import register_route, emit


# =============================
# ENTRYPOINT
# =============================

def transpile(ast):
    """
    Recebe AST e retorna código Python
    """

    lines = []

    # imports obrigatórios
    lines.append("from katlazapp.runtime.core import register_route, emit")
    lines.append("")

    for node in ast:
        if node["type"] == "route":
            lines.extend(transpile_route(node))
            lines.append("")

    return "\n".join(lines)


# =============================
# ROUTE
# =============================

def transpile_route(node):
    """
    Transpila uma rota
    """

    name = node["name"]
    params = node.get("params", [])

    # assinatura
    if params:
        args = ", ".join(params)
        header = f"def route_{name}({args}):"
    else:
        header = f"def route_{name}(data):"

    body = []

    # corpo
    for stmt in node.get("body", []):
        body.extend(transpile_statement(stmt))

    if not body:
        body.append("    pass")

    # registro da rota
    register = f'register_route("{name}", route_{name})'

    return [header] + body + ["", register]


# =============================
# STATEMENTS
# =============================

def transpile_statement(stmt):
    t = stmt["type"]

    if t == "emit":
        return [transpile_emit(stmt)]

    if t == "return":
        return [transpile_return(stmt)]

    if t == "expr":
        return [f"    {stmt['value']}"]

    return [f"    # Unknown statement: {t}"]


# =============================
# EMIT
# =============================

def transpile_emit(stmt):
    event = stmt["event"]
    data = stmt.get("data")

    if isinstance(data, str):
        return f'    emit("{event}", "{data}")'

    if data is None:
        return f'    emit("{event}")'

    return f'    emit("{event}", {repr(data)})'


# =============================
# RETURN
# =============================

def transpile_return(stmt):
    value = stmt.get("value")

    if isinstance(value, str):
        return f'    return "{value}"'

    return f"    return {repr(value)}"
