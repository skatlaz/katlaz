import sqlite3

conn = sqlite3.connect("katlaz.db", check_same_thread=False)
conn.row_factory = sqlite3.Row


def query(sql, params=()):
    cur = conn.execute(sql, params)
    conn.commit()
    return [dict(r) for r in cur.fetchall()]


def execute(sql, params=()):
    cur = conn.execute(sql, params)
    conn.commit()
    return cur.lastrowid

def select(table):
    return [dict(r) for r in conn.execute(f"SELECT * FROM {table}")]

def insert(table, data):
    keys = ", ".join(data.keys())
    qs = ", ".join(["?"] * len(data))

    cur = conn.execute(
        f"INSERT INTO {table} ({keys}) VALUES ({qs})",
        tuple(data.values())
    )

    conn.commit()
    return cur.lastrowid

class Model:
    table = None

    @classmethod
    def all(cls):
        return query(f"SELECT * FROM {cls.table}")

    @classmethod
    def create(cls, **data):
        keys = ", ".join(data.keys())
        qs = ", ".join(["?"] * len(data))
        return execute(
            f"INSERT INTO {cls.table} ({keys}) VALUES ({qs})",
            tuple(data.values())
        )
