# FILE: compiler/transpiler.py

def transpile(ast):
    code = ["def register(rt):"]

    functions = []

    for node in ast:
        if node["type"] == "route":
            name = node["name"]
            functions.append(name)

            code.append(f"    def {name}(data):")

        elif node["type"] == "print":
            code.append(f"        print({node['value']})")

    for fn in functions:
        code.append(f"    rt.register('{fn}', {fn})")

    return "\n".join(code)
