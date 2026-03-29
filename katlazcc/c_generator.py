#c_generator.py

# codegen/c_generator.py

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


