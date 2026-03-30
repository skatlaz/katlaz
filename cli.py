# katlaz/cli.py

import sys
from katlazcc.builder.build import build

def main():
    if len(sys.argv) < 2:
        print("Uso: katlaz build <arquivo.katlaz>")
        return

    comando = sys.argv[1]

    if comando == "build":
        arquivo = sys.argv[2]
        build(arquivo)

    else:
        print("Comando desconhecido")
