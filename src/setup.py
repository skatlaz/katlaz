from setuptools import setup
from Cython.Build import cythonize

setup(
    name="katlaz",
    ext_modules=cythonize("katlaz.pyx"),
    entry_points={
        "console_scripts": [
            "katlaz=katlaz:main"
        ]
    }
)
