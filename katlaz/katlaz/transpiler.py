#transpiler.py

def transpile_cython(ast):
    code = ""

    for node in ast:
        code += f"cpdef {node.name}():\n"
        code += "    pass\n\n"

    return codigo
