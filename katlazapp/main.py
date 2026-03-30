# FILE: katlazapp/main.py

import sys
import os
from pathlib import Path

# imports centralizados do seu __init__
from katlazapp import (
    parse_katlaz,
    transpile,
    handle,
)

# =============================
# COMPILER
# =============================

def compile_file(file_path: str):
    path = Path(file_path)

    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    ast = parse_katlaz(code)
    py_code = transpile(ast)

    output = path.with_suffix(".py")

    with open(output, "w", encoding="utf-8") as f:
        f.write(py_code)

    print(f"✅ Compiled: {output}")


# =============================
# RUNTIME EXECUTION
# =============================

def run_runtime():
    print("🚀 Katlaz runtime started")

    try:
        while True:
            cmd = input("katlaz> ")

            if cmd in ["exit", "quit"]:
                break

            payload = {
                "name": cmd,
                "data": {}
            }

            import json
            result = handle(json.dumps(payload))

            if result:
                print("→", result)

    except KeyboardInterrupt:
        print("\n⛔ Runtime stopped")


# =============================
# PROJECT CREATE
# =============================

def create_project(name: str):
    base = Path(name)

    dirs = ["app", "pcl", "compiler", "runtime"]

    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)

    # basic katlaz file
    with open(base / "main.katlaz", "w") as f:
        f.write(
"""route hello:
    print "Hello Katlaz"
"""
        )

    print(f"✅ Project '{name}' created")


# =============================
# CLI ENTRYPOINT
# =============================

def main():
    args = sys.argv

    if len(args) < 2:
        print("Katlaz CLI")
        print("Commands:")
        print("  create <name>")
        print("  build <file.katlaz>")
        print("  run")
        return

    cmd = args[1]

    if cmd == "create":
        if len(args) < 3:
            print("Usage: katlaz create <name>")
            return
        create_project(args[2])

    elif cmd == "build":
        if len(args) < 3:
            print("Usage: katlaz build <file.katlaz>")
            return
        compile_file(args[2])

    elif cmd == "run":
        run_runtime()

    else:
        print(f"❌ Unknown command: {cmd}")


# =============================
# ENTRY
# =============================

if __name__ == "__main__":
    main()
