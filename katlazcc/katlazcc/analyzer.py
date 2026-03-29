#analyzer.py

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}

    def visit_var_decl(self, node):
        if node.name in self.symbols:
            raise Exception(f"Variable is defined: {node.name}")

        self.symbols[node.name] = node.var_type

    def visit(self, node):
        method = getattr(self, f"visit_{type(node).__name__.lower()}", None)
        if method:
            method(node)
