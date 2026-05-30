"""Native interop helpers for KatlazApp.

Python bridge:
    py.call "math.sqrt", 9
C/C++ bridge via shared library:
    cpp.call "./libdemo.so", "add", 2, 3
"""
from __future__ import annotations

import ctypes
import importlib
from typing import Any


def call_python(path: str, *args: Any, **kwargs: Any) -> Any:
    if "." not in path:
        raise ValueError("Use 'module.function' for py.call")
    module_name, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)
    return func(*args, **kwargs)


def _ctype_value(value: Any):
    if isinstance(value, bool):
        return ctypes.c_bool(value)
    if isinstance(value, int):
        return ctypes.c_longlong(value)
    if isinstance(value, float):
        return ctypes.c_double(value)
    if isinstance(value, str):
        return ctypes.c_char_p(value.encode("utf-8"))
    return value


def call_cpp(library_path: str, function_name: str, *args: Any) -> Any:
    """Call a C ABI exported function from a C/C++ shared library.

    C++ functions must be exported as extern "C" to avoid name mangling.
    The default return type is long long. For richer native APIs, expose a C shim.
    """
    lib = ctypes.CDLL(library_path)
    func = getattr(lib, function_name)
    func.restype = ctypes.c_longlong
    return func(*[_ctype_value(a) for a in args])
