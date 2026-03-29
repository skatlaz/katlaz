#lexer.py

import re

TOKEN_SPEC = [
    ("NUMBER", r"\d+"),
    ("ID", r"[a-zA-Z_]\w*"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("COLON", r":"),
    ("ARROW", r"->"),
    ("COMMA", r","),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
]

def tokenize(code):
    tokens = []
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind != "SKIP":
            tokens.append((kind, value))

    return tokens
