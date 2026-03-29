    class Array:
        def __init__(self, elements):
            self.elements = elements

    class ArrayAccess:
        def __init__(self, name, index):
            self.name = name
            self.index = index

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
