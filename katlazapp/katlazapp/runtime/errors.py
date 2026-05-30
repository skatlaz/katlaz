def error(message, code="ERROR", **extra):
    payload = {"error": message, "code": code}
    payload.update(extra)
    return payload
