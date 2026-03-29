# type_checker.py
from ast.nodes import *

class TypeChecker:
    def __init__(self):
        self.symbols = {}
        self.classes = {}
        self.generics = {}

    def visit(self, node):
        method = f"visit_{type(node).__name__}"
        return getattr(self, method)(node)

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        value_type = self.visit(node.value)
        if node.var_type.name != value_type.name:
            raise Exception(f"Type error: {node.var_type.name} != {value_type.name}")
        self.symbols[node.name] = node.var_type
        return node.var_type

    def visit_IntLiteral(self, node): return Type("int")
    def visit_FloatLiteral(self, node): return Type("float")
    def visit_StringLiteral(self, node): return Type("str")
    def visit_BoolLiteral(self, node): return Type("bool")

    def visit_ListLiteral(self, node):
        elem_types = [self.visit(e) for e in node.elements]
        if len(elem_types) == 0: return Type("List", [Type("Any")])
        t0 = elem_types[0]
        for t in elem_types:
            if t.name != t0.name:
                raise Exception("List elements must have same type")
        return Type("List", [t0])

    def visit_MapLiteral(self, node):
        key_types = [self.visit(k) for k, v in node.pairs]
        val_types = [self.visit(v) for k, v in node.pairs]
        k0 = key_types[0] if key_types else Type("Any")
        v0 = val_types[0] if val_types else Type("Any")
        for kt in key_types:
            if kt.name != k0.name: raise Exception("Map keys must have same type")
        for vt in val_types:
            if vt.name != v0.name: raise Exception("Map values must have same type")
        return Type("Map", [k0, v0])
