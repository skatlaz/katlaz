# FILE: runtime/loader.py

import importlib
import os

def load_modules(runtime):
    for file in os.listdir():
        if file.endswith(".py") and file != "__init__.py":
            name = file.replace(".py", "")
            try:
                module = importlib.import_module(name)
                if hasattr(module, "register"):
                    module.register(runtime)
                    print(f"Loaded: {name}")
            except Exception as e:
                print(f"Error loading {name}: {e}")
