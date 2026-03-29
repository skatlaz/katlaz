# 🚀 Katlaz Language

**Katlaz** is a compiled programming language that combines Python-like simplicity with C-level performance.
It transpiles `.katlaz` source code into C and compiles it into native executables.

---

## ✨ Features

* ⚡ Compiles to native binaries (via C)
* 🧠 Simple and readable syntax (Python-inspired)
* 🔒 Strong typing (`int`, `float`, `str`)
* 🔁 Control flow: `if`, `else`, `while`, `for`
* 🧩 Functions with typed arguments and return values
* 🖥️ CLI tool (`katlaz`) for building projects

---

## 📦 Installation

```bash
pip install katlaz
```

---

## 🚀 Quick Start

### 1. Create a file

```katlaz
func main() -> int:
    print("Hello, Katlaz!")
    return 0
```

---

### 2. Build

```bash
katlaz build main.katlaz
```

---

### 3. Run

```bash
./main
```

(Windows: `main.exe`)

---

## 🧠 Language Basics

### Variables

```katlaz
x:int = 10
y:float = 3.14
name:str = "Katlaz"
```

---

### Functions

```katlaz
func add(a:int, b:int) -> int:
    return a + b
```

---

### Conditionals

```katlaz
if x > 10:
    print(x)
else:
    print(0)
```

---

### Loops

#### While

```katlaz
while x < 5:
    print(x)
    x = x + 1
```

#### For

```katlaz
for i:int = 0; i < 5; i = i + 1:
    print(i)
```

---

### Print

```katlaz
print("Hello")
print(123)
```

---

## 🏗️ Compilation Pipeline

```text
.katlaz → AST → C code → Native binary
```

Katlaz uses a custom parser and generates optimized C code, which is compiled using a system C compiler (e.g. `gcc`).

---

## 📁 Project Structure

```text
project/
 ├── main.katlaz
 └── utils.katlaz
```

---

## ⚙️ CLI Commands

```bash
katlaz build <file.katlaz>
```

---

## ⚠️ Requirements

* Python 3.8+
* GCC or compatible C compiler

---

## 🧪 Example

```katlaz
func sum(a:int, b:int) -> int:
    return a + b

func main() -> int:
    result:int = sum(5, 3)

    if result > 5:
        print(result)
    else:
        print(0)

    return 0
```

---

## 🛣️ Roadmap

* [ ] Module system (`import`)
* [ ] Arrays / collections
* [ ] String improvements
* [ ] Type inference
* [ ] LLVM backend
* [ ] VS Code extension

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

MIT License

---

## 💡 Inspiration

Katlaz is inspired by:

* Python (simplicity)
* C (performance)
* Modern compiled languages

---

## ⭐ Support

If you like this project, consider giving it a star ⭐ on GitHub!

