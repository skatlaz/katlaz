# codegen.py - Katlaz -> C nativo (monomorfização)
from ast.nodes import *

class CodeGen:
    def __init__(self):
        self.lines = []
        self.indent = 0
        self.instantiated_funcs = {}
        self.instantiated_classes = {}

    def emit(self, line):
        self.lines.append("  " * self.indent + line)

    def generate(self, node):
        method = f"gen_{type(node).__name__}"
        return getattr(self, method)(node)

    def gen_Program(self, node):
        # Include standard headers
        self.emit("#include <stdio.h>")
        self.emit("#include <stdlib.h>")
        self.emit("#include <string.h>")
        self.emit("#include <stdbool.h>")
        self.emit("")
        for stmt in node.statements:
            self.generate(stmt)
        return "\n".join(self.lines)

    # --------------------------
    # Types mapping
    # --------------------------
    def map_type(self, type_obj):
        if type_obj.name == "int": return "int"
        if type_obj.name == "float": return "double"
        if type_obj.name == "str": return "char*"
        if type_obj.name == "bool": return "bool"
        if type_obj.name.startswith("List"):
            # List<T> -> struct List_T
            inner = type_obj.params[0].name
            return f"struct List_{inner}"
        if type_obj.name.startswith("Map"):
            # Map<K,V> -> struct Map_K_V
            k = type_obj.params[0].name
            v = type_obj.params[1].name
            return f"struct Map_{k}_{v}"
        return f"struct {type_obj.name}"  # classes

    # --------------------------
    # Variables and literals
    # --------------------------
    def gen_VarDecl(self, node):
        typ = self.map_type(node.var_type)
        val = self.expr(node.value)
        self.emit(f"{typ} {node.name} = {val};")

    def gen_Assign(self, node):
        val = self.expr(node.value)
        self.emit(f"{node.name} = {val};")

    def expr(self, node):
        if isinstance(node, IntLiteral): return str(node.value)
        if isinstance(node, FloatLiteral): return str(node.value)
        if isinstance(node, BoolLiteral): return "true" if node.value else "false"
        if isinstance(node, StringLiteral): return f'"{node.value}"'
        if isinstance(node, AttributeAccess):
            obj = self.expr(node.obj)
            return f"{obj}.{node.attr}"
        if isinstance(node, ArrayAccess):
            arr = self.expr(node.obj)
            idx = self.expr(node.index)
            return f"{arr}[{idx}]"
        if isinstance(node, BinOp):
            left = self.expr(node.left)
            right = self.expr(node.right)
            return f"({left} {node.op} {right})"
        if isinstance(node, ListLiteral):
            # assume List<int> for simplicity
            tmp = f"list_{id(node)}"
            self.emit(f"struct List_int {tmp};")
            self.emit(f"{tmp}.len = {len(node.elements)};")
            self.emit(f"{tmp}.data = malloc(sizeof(int)*{len(node.elements)});")
            for i, e in enumerate(node.elements):
                self.emit(f"{tmp}.data[{i}] = {self.expr(e)};")
            return tmp
        if isinstance(node, MapLiteral):
            # assume Map<str,int> for simplicity
            tmp = f"map_{id(node)}"
            self.emit(f"struct Map_str_int {tmp};")
            self.emit(f"{tmp}.len = {len(node.pairs)};")
            self.emit(f"{tmp}.keys = malloc(sizeof(char*)*{len(node.pairs)});")
            self.emit(f"{tmp}.values = malloc(sizeof(int)*{len(node.pairs)});")
            for i, (k, v) in enumerate(node.pairs):
                self.emit(f"{tmp}.keys[{i}] = strdup({self.expr(k)});")
                self.emit(f"{tmp}.values[{i}] = {self.expr(v)};")
            return tmp
        if isinstance(node, FuncCall):
            args = ", ".join([self.expr(a) for a in node.args])
            return f"{node.name}({args})"
        if isinstance(node, VarDecl):
            return node.name
        if isinstance(node, str):
            return node
        return "/* unsupported expr */"

    # --------------------------
    # Functions (monomorfização)
    # --------------------------
    def gen_Func(self, node):
        # monomorphized function
        ret_type = self.map_type(node.return_type) if node.return_type else "void"
        args = ", ".join([f"{self.map_type(a.var_type)} {a.name}" for a in node.args])
        self.emit(f"{ret_type} {node.name}({args}) {{")
        self.indent += 1
        for stmt in node.body:
            self.generate(stmt)
        self.indent -= 1
        self.emit("}")

    # --------------------------
    # Classes genéricas
    # --------------------------
    def gen_Class(self, node):
        name = node.name
        type_param = node.type_param
        struct_name = f"{name}_{type_param}" if type_param else name
        self.emit(f"struct {struct_name} {{")
        self.indent += 1
        for f in node.fields:
            f_type = self.map_type(f.var_type)
            self.emit(f"{f_type} {f.name};")
        self.indent -= 1
        self.emit("};\n")
        # constructor
        if node.constructor:
            args = ", ".join([f"{self.map_type(a.var_type)} {a.name}" for a in node.constructor.args])
            self.emit(f"void {struct_name}_start(struct {struct_name}* self, {args}) {{")
            self.indent += 1
            for stmt in node.constructor.body:
                self.generate(stmt)
            self.indent -= 1
            self.emit("}\n")

    # --------------------------
    # Print helper
    # --------------------------
    def gen_Expr(self, node):
        code = self.expr(node)
        self.emit(f"printf(\"%d\\n\", {code});")  # simplified for int

    # --------------------------
    # Return
    # --------------------------
    def gen_ReturnStmt(self, node):
        self.emit(f"return {self.expr(node.value)};")
