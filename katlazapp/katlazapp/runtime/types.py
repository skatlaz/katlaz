def validate_type(value, typ):
    if typ == "string":
        return isinstance(value, str)

    if typ == "int":
        return isinstance(value, int)

    if typ == "bool":
        return isinstance(value, bool)

    if typ == "float":
        return isinstance(value, float)

    if typ == "any":
        return True

    return False


def cast_type(value, typ):
    try:
        if typ == "int":
            return int(value)

        if typ == "float":
            return float(value)

        if typ == "bool":
            return bool(value)

        if typ == "string":
            return str(value)

    except:
        return value

    return value
