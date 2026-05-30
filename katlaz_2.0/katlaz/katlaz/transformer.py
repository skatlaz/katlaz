# transformer.py - Parse Tree -> AST
from lark import Transformer
from ast.nodes import *

class KatlazTransformer(Transformer):
    def start(self, items):
        return Program(items)

    def var_decl(self, items):
        return VarDecl(items[0], items[1], items[2])

    def assign(self, items):
        return Assign(items[0], items[1])

    def generic_type(self, items):
        return Type(items[0], [items[1]])

    def array_type(self, items):
        return Type(items[0], is_array=True)

    def int_lit(self, items):
        return IntLiteral(int(items[0]))

    def float_lit(self, items):
        return FloatLiteral(float(items[0]))

    def string_lit(self, items):
        return StringLiteral(str(items[0])[1:-1])

    def true(self, _): return BoolLiteral(True)
    def false(self, _): return BoolLiteral(False)

    def list_expr(self, items):
        return ListLiteral(items)

    def map_expr(self, items):
        return MapLiteral(items)

    def map_item(self, items):
        return (items[0], items[1])

    def func_def(self, items):
        name = items[0]
        type_params = [items[1]] if len(items) > 4 else []
        args = items[2]
        return_type = items[3] if len(items) > 3 else None
        body = items[-1]
        return Func(name, type_params, args, return_type, body)

    def constructor(self, items):
        args = items[0] if items else []
        body = items[-1]
        return Constructor(args, body)

    def class_def(self, items):
        name = items[0]
        type_param = items[1] if isinstance(items[1], str) else None
        body = items[-1]
        fields, methods, constructor = [], [], None
        for item in body:
            if isinstance(item, VarDecl):
                fields.append(item)
            elif isinstance(item, Func):
                methods.append(item)
            elif isinstance(item, Constructor):
                constructor = item
        return Class(name, type_param, fields, methods, constructor)
