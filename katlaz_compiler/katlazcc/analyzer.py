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

    def visit_SqliteOpen(self, node):
        db_name = "db_conn"

        self.emit('PyObject *sqlite3 = PyImport_ImportModule("sqlite3");')
        self.emit(f'PyObject *{db_name} = PyObject_CallMethod(sqlite3, "connect", "s", "{node.filename}");')
        
    def visit_SqliteExec(self, node):
        self.emit(f'PyObject_CallMethod({node.db_var}, "execute", "s", "{node.query}");')
        self.emit(f'PyObject_CallMethod({node.db_var}, "commit", NULL);')

    def visit_Print(self, node):
        if self.is_python_object(node.value):
            self.emit(f'PyObject_Print({self.expr(node.value)}, stdout, 0);')
            self.emit('printf("\\n");')
        else:
            self.emit(f'printf("%d\\n", {self.expr(node.value)});')
