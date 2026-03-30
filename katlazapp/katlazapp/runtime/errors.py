def error(message, code="KATLAZ_ERROR", hint=None):
    return {
        "error": message,
        "code": code,
        "hint": hint
    }
