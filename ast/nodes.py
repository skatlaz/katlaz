# ast_nodes.py

class Program:
    def __init__(self, statements):
        self.statements = statements


class FuncDef:
    def __init__(self, name, args, return_type, body):
        self.name = name
        self.args = args
        self.return_type = return_type
        self.body = body


class VarDecl:
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value


class Return:
    def __init__(self, value):
        self.value = value


class Print:
    def __init__(self, value):
        self.value = value


class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Number:
    def __init__(self, value):
        self.value = value


class String:
    def __init__(self, value):
        self.value = value


class Var:
    def __init__(self, name):
        self.name = name


class FuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class If:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class For:
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value
