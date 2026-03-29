# katlaz/cli.py

import sys
from katlaz.builder.build import build

def main():
    if len(sys.argv) < 2:
        print("Use: katlazcc compile <arquivo.katlaz>")
        return

    comando = sys.argv[1]

    if comando == "compile":
        arquivo = sys.argv[2]
        build(arquivo)

    else:
        print("Command unknow")
