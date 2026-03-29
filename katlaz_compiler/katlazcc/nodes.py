# =========================
# CORE PROGRAM
# =========================

class Program:
    def __init__(self, statements):
        self.statements = statements


# =========================
# FUNÇÕES
# =========================

class FuncDef:
    def __init__(self, name, args, return_type, body):
        self.name = name
        self.args = args
        self.return_type = return_type
        self.body = body


class Return:
    def __init__(self, value):
        self.value = value


# =========================
# VARIÁVEIS
# =========================

class VarDecl:
    def __init__(self, name, var_type, value):
        self.name = name
        self.var_type = var_type
        self.value = value


class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Var:
    def __init__(self, name):
        self.name = name


# =========================
# TIPOS BÁSICOS
# =========================

class Number:
    def __init__(self, value):
        self.value = value


class String:
    def __init__(self, value):
        self.value = value


# =========================
# EXPRESSÕES
# =========================

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


# =========================
# PRINT
# =========================

class Print:
    def __init__(self, value):
        self.value = value


# =========================
# CONTROLE DE FLUXO
# =========================

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


# =========================
# FUNÇÃO CALL
# =========================

class FuncCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args


# =========================
# ARRAYS
# =========================

class Array:
    def __init__(self, elements):
        self.elements = elements


class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index


# =========================
# SQLITE (PYTHON EMBED)
# =========================

class SqliteOpen:
    def __init__(self, filename):
        self.filename = filename


class SqliteExec:
    def __init__(self, db_var, query):
        self.db_var = db_var
        self.query = query


class SqliteQuery:
    def __init__(self, db_var, query):
        self.db_var = db_var
        self.query = query


# =========================
# PYTHON INTEROP (PYPI)
# =========================

class PyImport:
    def __init__(self, module):
        self.module = module


class PyCall:
    def __init__(self, func, args):
        self.func = func
        self.args = args


# =========================
# ORM (MODELOS)
# =========================

class Model:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class Field:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_


# =========================
# ORM OPERAÇÕES
# =========================

class ModelCreateTable:
    def __init__(self, model):
        self.model = model


class ModelInsert:
    def __init__(self, model, args):
        self.model = model
        self.args = args


class ModelAll:
    def __init__(self, model):
        self.model = model


class ModelFilter:
    def __init__(self, model, condition):
        self.model = model
        self.condition = condition


class ModelUpdate:
    def __init__(self, model, condition, updates):
        self.model = model
        self.condition = condition
        self.updates = updates


class ModelDelete:
    def __init__(self, model, condition):
        self.model = model
        self.condition = condition
