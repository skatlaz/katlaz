# parser.py

from lark import Lark, Transformer
from ast_nodes import *

with open("grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")


class KatlazTransformer(Transformer):

    def program(self, items):
        return Program(items)

    def func_def(self, items):
        name = items[0]
        args = items[1] if isinstance(items[1], list) else []
        return_type = items[-2]
        body = items[-1]
        return FuncDef(name, args, return_type, body)

    def args(self, items):
        return items

    def arg(self, items):
        return (items[0], items[1])

    def var_decl(self, items):
        return VarDecl(items[0], items[1], items[2])

    def return_stmt(self, items):
        return Return(items[0])

    def print_stmt(self, items):
        return Print(items[0])

    def add(self, items):
        return BinOp(items[0], "+", items[1])

    def sub(self, items):
        return BinOp(items[0], "-", items[1])

    def mul(self, items):
        return BinOp(items[0], "*", items[1])

    def div(self, items):
        return BinOp(items[0], "/", items[1])

    def number(self, items):
        return Number(int(items[0]))

    def string(self, items):
        return String(items[0][1:-1])

    def var(self, items):
        return Var(str(items[0]))

    def func_call(self, items):
        name = items[0]
        args = items[1] if len(items) > 1 else []
        return FuncCall(name, args)

    def args_call(self, items):
        return items

    def NAME(self, token):
        return str(token)

    def type(self, token):
        return str(token[0])

    def sqlite_open(self, items):
        return SqliteOpen(items[1])

    def sqlite_exec(self, items):
        return SqliteExec(items[0], items[1])

    def sqlite_query(self, items):
        return SqliteQuery(items[0], items[1])

    def is_python_object(self, node):
        return isinstance(node, SqliteQuery)

def parse(code):
    tree = parser.parse(code)
    return KatlazTransformer().transform(tree)
    
def teste():
#    from parser import parse

    codigo = """
    func soma(a:int, b:int) -> int:
        return a + b

    func main() -> int:
        x:int = soma(2, 3)
        print(x)
        return 0
    """

    ast = parse(codigo)

    print(ast)

def if_stmt(self, items):
    condition = items[0]
    then_block = items[1]
    else_block = items[2] if len(items) > 2 else None
    return If(condition, then_block, else_block)


def while_stmt(self, items):
    return While(items[0], items[1])


def for_stmt(self, items):
    return For(items[0], items[1], items[2], items[3])


def assign_stmt(self, items):
    return Assign(items[0], items[1])


# comparações
def eq(self, items): return BinOp(items[0], "==", items[1])
def ne(self, items): return BinOp(items[0], "!=", items[1])
def lt(self, items): return BinOp(items[0], "<", items[1])
def gt(self, items): return BinOp(items[0], ">", items[1])
def le(self, items): return BinOp(items[0], "<=", items[1])
def ge(self, items): return BinOp(items[0], ">=", items[1])
