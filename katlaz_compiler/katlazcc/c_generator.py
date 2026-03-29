#c_generator.py
#include <Python.h>

def generate(self, ast):
    self.emit("#include <Python.h>")
    self.emit("#include <stdio.h>")
    self.emit("")

    self.emit("int main() {")
    self.indent += 1

    self.emit("Py_Initialize();")
    self.emit("")

class CGenerator:
    
    def __init__(self):
        self.code = []
        self.indent = 0

    def emit(self, line):
        self.code.append("    " * self.indent + line)

    def generate(self, ast):
        self.emit("#include <stdio.h>")
        self.emit("")

        for stmt in ast.statements:
            self.visit(stmt)

        return "\n".join(self.code)

    def visit_funcdef(self, node):
        args = ", ".join([f"int {a[0]}" for a in node.args])

        self.code.append(f"int {node.name}({args}) {{")

        for stmt in node.body:
            self.visit(stmt)

        self.code.append("}\n")

    def visit_vardecl(self, node):
        self.code.append(f"int {node.name} = {node.value};")

    def visit_print(self, value):
        self.code.append(f'printf("%d\\n", {value});')
        
    def visit_if(self, node):
        self.code.append(f"if ({self.expr(node.condition)}) {{")

        for stmt in node.then_block:
            self.visit(stmt)

        self.code.append("}")

        if node.else_block:
            self.code.append("else {")
            for stmt in node.else_block:
                self.visit(stmt)
            self.code.append("}")

    def visit_while(self, node):
        self.code.append(f"while ({self.expr(node.condition)}) {{")

        for stmt in node.body:
            self.visit(stmt)

        self.code.append("}")

    def visit_for(self, node):
        init = f"int {node.init.name} = {self.expr(node.init.value)}"
        cond = self.expr(node.condition)
        update = f"{node.update.name} = {self.expr(node.update.value)}"

        self.code.append(f"for ({init}; {cond}; {update}) {{")

        for stmt in node.body:
            self.visit(stmt)

        self.code.append("}")

    def visit_assign(self, node):
        self.code.append(f"{node.name} = {self.expr(node.value)};")

    def expr(self, node):
        if isinstance(node, BinOp):
            return f"({self.expr(node.left)} {node.op} {self.expr(node.right)})"
        elif isinstance(node, Number):
            return str(node.value)
        elif isinstance(node, Var):
            return node.name

    def visit_Array(self, node):
        values = ", ".join(self.expr(e) for e in node.elements)
        return f"{{{values}}}"


    def expr(self, node):
        if isinstance(node, ArrayAccess):
            return f"{node.name}[{self.expr(node.index)}]"
        if isinstance(node, SqliteQuery):
            return self.generate_sqlite_query(node)
        elif isinstance(node, ArrayAccess):
            return f"PyList_GetItem({node.name}, {index})"

    def visit_PyList(self, node):
        self.emit("PyObject* lista = PyList_New(0);")

    def visit_PyImport(self, node):
        self.emit(f'PyImport_ImportModule("{node.module}");')

def generate_sqlite_query(self, node):
    var_name = f"query_result_{id(node)}"

    self.emit(f'PyObject *{var_name}_cursor = PyObject_CallMethod({node.db_var}, "execute", "s", "{node.query}");')
    self.emit(f'PyObject *{var_name} = PyObject_CallMethod({var_name}_cursor, "fetchall", NULL);')

    return var_name



self.emit("Py_Finalize();")
self.emit("return 0;")
self.indent -= 1
self.emit("}")
