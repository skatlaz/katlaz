# FILE: runtime/bridge.py

from runtime.core import KatlazRuntime
from runtime.loader import load_modules

runtime = KatlazRuntime()
load_modules(runtime)

def handle(payload):
    return runtime.handle(payload)
