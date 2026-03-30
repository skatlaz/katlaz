from setuptools import setup, find_packages

setup(
    name="katlazapp",
    version="0.1.0",
    packages=find_packages(),  # <- importante
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "katlazapp=katlazapp.cli:main"
        ]
    },
)
