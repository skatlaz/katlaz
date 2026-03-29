# ast/nodes.py - Katlaz AST

class Node:
    pass

class Program(Node):
    def __init__(self, statements):
        self.statements = statements

class VarDecl(Node):
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value

class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Type(Node):
    def __init__(self, name, params=None, is_array=False):
        self.name = name
        self.params = params or []
        self.is_array = is_array
    def __repr__(self):
        if self.params:
            return f"{self.name}<{self.params}>"
        return self.name

class Literal(Node):
    def __init__(self, value):
        self.value = value

class IntLiteral(Literal): pass
class FloatLiteral(Literal): pass
class StringLiteral(Literal): pass
class BoolLiteral(Literal): pass

class ListLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

class MapLiteral(Node):
    def __init__(self, pairs):
        self.pairs = pairs

class Expr(Node): pass

class AttributeAccess(Expr):
    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

class ArrayAccess(Expr):
    def __init__(self, obj, index):
        self.obj = obj
        self.index = index

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Neg(Expr):
    def __init__(self, expr):
        self.expr = expr

class FuncCall(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Func(Node):
    def __init__(self, name, type_params, args, return_type, body):
        self.name = name
        self.type_params = type_params
        self.args = args
        self.return_type = return_type
        self.body = body

class GenericFuncInstance(Node):
    def __init__(self, generic_func, concrete_types):
        self.generic_func = generic_func
        self.concrete_types = concrete_types

class Class(Node):
    def __init__(self, name, type_param=None, fields=None, methods=None, constructor=None):
        self.name = name
        self.type_param = type_param
        self.fields = fields or []
        self.methods = methods or []
        self.constructor = constructor

class Constructor(Node):
    def __init__(self, args, body):
        self.args = args
        self.body = body
