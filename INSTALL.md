# 📦 Katlaz Installation & Build Guide (pip + compiler separation)

This guide explains how to:

* 📥 Download the Katlaz repository from GitHub
* 🏗️ Build the project using `pip -m build`
* 📦 Install it locally using `pip install .`
* ⚙️ Build and install the **compiler separately**

Repository:
👉 https://github.com/skatlaz/katlaz

---

# 📥 1. Clone the Repository

```bash
git clone https://github.com/skatlaz/katlaz.git
cd katlaz
```

---

# 🧱 2. Python Build System Setup

Make sure you have the required tools:

```bash
pip install --upgrade pip
pip install build setuptools wheel
```

---

# 📦 3. Basic Project Build (Full Package)

Inside the root folder:

```bash
python -m build
```

This will generate:

```bash
dist/
 ├── katlaz-<version>.tar.gz
 └── katlaz-<version>-py3-none-any.whl
```

---

# 📥 4. Install Locally

```bash
pip install .
```

Or install from built wheel:

```bash
pip install dist/*.whl
```

---

# 🚀 5. Using Katlaz CLI

After installation:

```bash
katlaz create my_app
katlaz build
katlaz serve
```

---

# ⚙️ 6. Compiler Separation (IMPORTANT)

The repository contains a **compiler subsystem** located at:

```bash
katlaz/katlaz/
```

This includes:

* language parsing
* transpiler
* machine-level compilation logic

👉 To make this modular and installable via pip, we separate it as a package.

---

# 📁 Recommended Structure for Compiler Packaging

```bash
katlaz/
│
├── katlaz/                # CLI + runtime
│
├── katlaz_compiler/       # NEW package (recommended)
│   ├── __init__.py
│   ├── parser.py
│   ├── transpiler.py
│   ├── backend/
│   └── core/
│
├── pyproject.toml
```

---

# 🧱 7. Create `pyproject.toml` (Root)

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "katlaz"
version = "0.1.0"
description = "Katlaz Framework"
authors = [{name="Katlaz"}]
dependencies = []
```

---

# ⚙️ 8. Separate Compiler Package

## 📄 `katlaz_compiler/pyproject.toml`

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "katlaz-compiler"
version = "0.1.0"
description = "Katlaz Language Compiler"
authors = [{name="Katlaz"}]
dependencies = []
```

---

# 🏗️ 9. Build Compiler Only

Navigate to compiler package:

```bash
cd katlaz_compiler
python -m build
```

---

# 📦 10. Install Compiler Separately

```bash
pip install .
```

Now you can import it independently:

```python
import katlaz_compiler
```

---

# 🔗 11. Linking CLI with Compiler

Inside your CLI (`katlaz.pyx` or `katlaz.py`):

```python
from katlaz_compiler.parser import parse_katlaz
from katlaz_compiler.transpiler import transpile
```

👉 This keeps architecture clean and modular.

---

# 🧪 12. Optional: Editable Mode (Dev)

For development:

```bash
pip install -e .
```

And for compiler:

```bash
cd katlaz_compiler
pip install -e .
```

---

# 🧠 13. Advanced: Multiple Packages in One Repo

You can manage both packages:

```bash
pip install ./katlaz
pip install ./katlaz_compiler
```

---

# 🔥 14. Recommended Workflow

```bash
git clone https://github.com/skatlaz/katlaz.git

# install compiler first
cd katlaz_compiler
pip install -e .

# install main framework
cd ..
pip install -e .
```

---

# ⚠️ Notes

* Keep compiler independent → easier to maintain
* Allows reuse in other projects
* Enables future publishing to PyPI

---

# 🚀 Future Improvements

* Publish `katlaz` and `katlaz-compiler` to PyPI
* Add versioning compatibility
* Add CLI command:

```bash
katlaz compile file.katlaz
```

---

# 💥 Conclusion

You now have:

* 📦 Full Katlaz install via pip
* ⚙️ Independent compiler package
* 🧠 Clean modular architecture

---

👉 This setup turns Katlaz into a **real distributable framework**
👉
