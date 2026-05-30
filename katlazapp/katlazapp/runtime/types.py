def validate_type(value, typ):
    if typ in (None, "", "any"):
        return True
    if value is None:
        return False
    if typ in ("int", "integer"):
        try: int(value); return True
        except Exception: return False
    if typ in ("float", "double"):
        try: float(value); return True
        except Exception: return False
    if typ in ("str", "string"):
        return isinstance(value, str)
    if typ == "bool":
        return isinstance(value, bool) or str(value).lower() in {"true", "false", "1", "0"}
    return True


def cast_type(value, typ):
    if typ in (None, "", "any"):
        return value
    if typ in ("int", "integer"):
        return int(value)
    if typ in ("float", "double"):
        return float(value)
    if typ in ("str", "string"):
        return str(value)
    if typ == "bool":
        if isinstance(value, bool): return value
        return str(value).lower() in {"true", "1"}
    return value
