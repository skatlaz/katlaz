# builder.py

from katlazcc.parser import parse
from .katlazcc.codegen.c_generator import CGenerator
import subprocess
from pathlib import Path

def compile(file):
    path = Path(file)
    code = path.read_text()

    ast = parse(code)

    generator = CGenerator()
    c_code = generator.generate(ast)

    c_file = path.with_suffix(".c")
    c_file.write_text(c_code)

    output = path.stem

    subprocess.run(["gcc", str(c_file), "-o", output], check=True)

    print(f"✅ Exec created: {output}")
