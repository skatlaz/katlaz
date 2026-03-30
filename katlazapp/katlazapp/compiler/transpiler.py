# =============================
# IMPORTS DO RUNTIME
# =============================
# Essas funções serão usadas no código gerado
# (não são usadas diretamente aqui, mas o código final precisa delas)
from katlazapp.runtime.core import register_route, emit
from katlazapp.runtime.types import validate_type, cast_type
from katlazapp.runtime.db import insert, select, conn
from katlazapp.runtime.fs import read, write
from katlazapp.runtime.errors import error


# =============================
# ENTRYPOINT
# =============================
def transpile(ast):
    """
    Recebe AST do parser e gera código Python executável
    """

    # Cabeçalho do arquivo gerado (imports necessários)
    lines = [
        "from katlazapp.runtime.core import register_route, emit",
        "from katlazapp.runtime.types import validate_type, cast_type",
        "from katlazapp.runtime.db import insert, select, conn",
        "from katlazapp.runtime.fs import read, write",
        "from katlazapp.runtime.errors import error",
        ""
    ]

    # Percorre todos os nós do AST
    for node in ast:
        if node["type"] == "model":
            lines.extend(transpile_model(node))

        elif node["type"] == "route":
            lines.extend(transpile_route(node))

    # Junta tudo em string final
    return "\n".join(lines)


# =============================
# MODEL → SQL AUTOMÁTICO
# =============================
def transpile_model(node):
    """
    Converte:
    model users:
        id int
        name string

    Em:
    CREATE TABLE IF NOT EXISTS users (...)
    """

    name = node["name"]

    fields = []
    for f in node["fields"]:
        # Mapeamento de tipos Katlaz → SQLite
        t = "TEXT"

        if f["type"] == "int":
            t = "INTEGER"

        if f["type"] == "bool":
            t = "INTEGER"

        if f["type"] == "float":
            t = "REAL"

        fields.append(f"{f['name']} {t}")

    # SQL final
    sql = f'CREATE TABLE IF NOT EXISTS {name} ({", ".join(fields)})'

    return [
        f'conn.execute("""{sql}""")',
        "conn.commit()",
        ""
    ]


# =============================
# ROUTE
# =============================
def transpile_route(node):
    """
    Converte rotas Katlaz em funções Python
    """

    name = node["name"]

    # Sempre usamos **data para flexibilidade
    header = f"def route_{name}(**data):"

    body = []

    # =============================
    # PARAMS COM TIPAGEM
    # =============================
    for p in node["params"]:
        param_name = p["name"]
        param_type = p["type"]

        # Pega valor do request
        body.append(f"    {param_name} = data.get('{param_name}')")

        # Validação de tipo
        body.append(f"""    if not validate_type({param_name}, "{param_type}"):
        return error("Invalid type for '{param_name}'", hint="Expected {param_type}")""")

        # Casting automático
        body.append(f"    {param_name} = cast_type({param_name}, '{param_type}')")

    # =============================
    # CORPO DA ROTA
    # =============================
    for stmt in node["body"]:
        body.extend(transpile_statement(stmt))

    # Se não houver return explícito
    if not any("return" in line for line in body):
        body.append("    return {}")

    # Registro automático da rota
    register = f'register_route("{name}", route_{name})'

    return [header] + body + ["", register, ""]


# =============================
# STATEMENTS
# =============================
def transpile_statement(stmt):
    """
    Converte cada linha do Katlaz em Python
    """

    t = stmt["type"]

    # =============================
    # EMIT
    # =============================
    if t == "emit":
        if stmt["data"]:
            return [f'    return emit("{stmt["event"]}", {stmt["data"]})']
        return [f'    return emit("{stmt["event"]}")']

    # =============================
    # VARIÁVEL
    # =============================
    if t == "assign":
        return [f"    {stmt['var']} = {stmt['expr']}"]

    # =============================
    # DB INSERT
    # =============================
    if t == "db_insert":
        pairs = stmt["data"].split(",")

        py_dict = "{"
        for p in pairs:
            k, v = p.split(":")
            py_dict += f'"{k.strip()}": {v.strip()},'
        py_dict += "}"

        return [f"    insert('{stmt['table']}', {py_dict})"]

    # =============================
    # DB SELECT
    # =============================
    if t == "db_select":
        return [f"    return select('{stmt['table']}')"]

    # =============================
    # FS READ
    # =============================
    if t == "fs_read":
        return [f"    return read('{stmt['path']}')"]

    # =============================
    # FS WRITE
    # =============================
    if t == "fs_write":
        return [f"    write('{stmt['path']}', '{stmt['content']}')"]

    # =============================
    # FALLBACK (código direto)
    # =============================
    return [f"    {stmt.get('value', '')}"]
