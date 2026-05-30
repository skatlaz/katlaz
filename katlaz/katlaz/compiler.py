import os
import subprocess
from .parser import parse_file
from .transformer import KatlazTransformer
from .type_checker import TypeChecker
from .codegen import CodeGen

def build(filename: str, output: str = None):
    """
    Compila arquivo .katlaz para binário nativo.
    """
    output = output or "a.out"
    
    # 1. Parse
    tree = parse_file(filename)
    
    # 2. AST
    transformer = KatlazTransformer()
    ast_root = transformer.transform(tree)
    
    # 3. Type check
    checker = TypeChecker()
    checker.visit(ast_root)
    
    # 4. Codegen
    cg = CodeGen()
    c_code = cg.generate(ast_root)
    
    c_file = "tmp_katlaz.c"
    with open(c_file, "w") as f:
        f.write(c_code)
    
    # 5. Compile com GCC/Clang
    if os.name == "nt":
        compiler = "gcc"  # ou clang no Windows
        exe_file = output + ".exe"
    else:
        compiler = "gcc"
        exe_file = output

    subprocess.run([compiler, c_file, "-o", exe_file])
    os.remove(c_file)
    print(f"Compiled {filename} -> {exe_file}")
