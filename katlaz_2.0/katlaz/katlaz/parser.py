from pathlib import Path
from lark import Lark, Transformer, v_args
from .ast.nodes import *

_GRAMMAR = r'''
start: statement*

?statement: func_def
          | var_decl
          | assign_stmt
          | print_stmt
          | return_stmt
          | if_stmt
          | while_stmt
          | expr

func_def: "func" NAME "(" params? ")" ("->" type)? ":" block
params: param ("," param)*
param: NAME ":" type

block: statement+

var_decl: NAME ":" type "=" expr
assign_stmt: NAME "=" expr
print_stmt: "print" expr
return_stmt: "return" expr
if_stmt: "if" expr ":" block ("else" ":" block)?
while_stmt: "while" expr ":" block

?expr: comparison
?comparison: sum (COMP_OP sum)*
?sum: product (ADD_OP product)*
?product: atom (MUL_OP atom)*
?atom: NUMBER           -> number
     | STRING           -> string
     | NAME "(" call_args? ")" -> func_call
     | NAME             -> var
     | "(" expr ")"

call_args: expr ("," expr)*
type: NAME

COMP_OP: "=="|"!="|"<="|">="|"<"|">"
ADD_OP: "+"|"-"
MUL_OP: "*"|"/"

%import common.CNAME -> NAME
%import common.SIGNED_NUMBER -> NUMBER
%import common.ESCAPED_STRING -> STRING
%import common.WS
%ignore WS
%ignore /#.*/
'''

parser = Lark(_GRAMMAR, parser="lalr")

class Print(Node):
    def __init__(self, value): self.value = value

class Return(Node):
    def __init__(self, value): self.value = value

class If(Node):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition; self.then_block = then_block; self.else_block = else_block

class While(Node):
    def __init__(self, condition, body): self.condition = condition; self.body = body

class Var(Expr):
    def __init__(self, name): self.name = name

class FuncDef(Node):
    def __init__(self, name, args, return_type, body):
        self.name = name; self.args = args; self.return_type = return_type; self.body = body

@v_args(inline=True)
class KatlazTransformer(Transformer):
    def start(self, *items): return Program(list(items))
    def block(self, *items): return list(items)
    def type(self, name): return Type(str(name))
    def param(self, name, typ): return {"name": str(name), "type": typ}
    def params(self, *items): return list(items)
    def func_def(self, name, *items):
        params, return_type, body = [], Type("void"), []
        if len(items) == 1:
            body = items[0]
        elif len(items) == 2:
            if isinstance(items[0], list): params = items[0]; body = items[1]
            else: return_type = items[0]; body = items[1]
        elif len(items) == 3:
            params, return_type, body = items
        return FuncDef(str(name), params, return_type, body)
    def var_decl(self, name, typ, value): return VarDecl(str(name), typ, value)
    def assign_stmt(self, name, value): return Assign(str(name), value)
    def print_stmt(self, value): return Print(value)
    def return_stmt(self, value): return Return(value)
    def if_stmt(self, condition, then_block, else_block=None): return If(condition, then_block, else_block)
    def while_stmt(self, condition, body): return While(condition, body)
    def number(self, token):
        s = str(token)
        return FloatLiteral(float(s)) if "." in s else IntLiteral(int(s))
    def string(self, token): return StringLiteral(str(token)[1:-1])
    def var(self, name): return Var(str(name))
    def func_call(self, name, args=None): return FuncCall(str(name), args or [])
    def call_args(self, *items): return list(items)
    def comparison(self, first, *rest): return self._fold(first, rest)
    def sum(self, first, *rest): return self._fold(first, rest)
    def product(self, first, *rest): return self._fold(first, rest)
    def _fold(self, first, rest):
        node = first
        for i in range(0, len(rest), 2):
            node = BinOp(node, str(rest[i]), rest[i+1])
        return node

def parse(code: str):
    tree = parser.parse(code)
    return KatlazTransformer().transform(tree)
