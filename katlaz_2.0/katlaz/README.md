# Katlaz Language

Katlaz is a compiled programming language that transforms `.katlaz` source code into optimized C and then compiles it into native binaries.

It combines modern language features such as generics, object-oriented programming, and strong typing with the performance of compiled languages like C/C++ and Rust.

---

## 🚀 Features

* ✅ Strong static typing (`int`, `float`, `str`, `bool`)
* ✅ Generics (`List<T>`, `Map<K,V>`)
* ✅ Object-Oriented Programming (classes, methods, constructors)
* ✅ Monomorphization (Rust-like performance)
* ✅ Native compilation (via C → GCC/Clang)
* ✅ Cross-platform (Windows, Linux, macOS)
* ✅ Optional SQLite ORM

---

## 📦 Installation

### Requirements

* Python 3.8+
* pip
* C compiler (GCC or Clang)

---

### Windows

1. Install Python: https://python.org
2. Install a C compiler:

   * MinGW **or**
   * Visual Studio Build Tools

Verify:

```
gcc --version
```

---

### Linux (Ubuntu/Debian)

```
sudo apt update
sudo apt install python3 python3-pip build-essential
```

---

### macOS

```
xcode-select --install
brew install python
```

---

### Install Katlaz

```
pip install katlaz
```

Or locally:

```
pip install .
```

Development mode:

```
pip install -e .
```

---

## ⚡ CLI Usage

```
katlaz <file.katlaz> -o <output_binary>
```

Example:

```
katlaz hello.katlaz -o hello
```

---

## ▶️ Running the Binary

### Linux / macOS

```
./hello
```

### Windows

```
hello.exe
```

---

## 🧠 Language Basics

---

### Variables

```
x:int = 10
y:float = 3.14
name:str = "John"
flag:bool = True
```

---

### If / Else

```
if x > 5:
    print(1)
else:
    print(0)
```

---

### While Loop

```
i:int = 0

while i < 5:
    print(i)
    i = i + 1
```

---

### For Loop

```
for i:int = 0; i < 5; i = i + 1:
    print(i)
```

---

## 🔁 Functions

```
func add(a:int, b:int) -> int:
    return a + b
```

---

## 🧬 Generics

### Generic Function

```
func identity<T>(x:T) -> T:
    return x
```

Usage:

```
a:int = identity(10)
```

---

## 🧱 Classes

```
class User:
    id:int
    name:str

    start(id:int, name:str):
        self.id = id
        self.name = name
```

Usage:

```
u:User = User(1, "John")
print(u.name)
```

---

## 🧩 Generic Classes

```
class Box<T>:
    value:T

    start(value:T):
        self.value = value
```

Usage:

```
b:Box<int> = Box(10)
print(b.value)
```

---

## 📦 Lists

```
nums:List<int> = [1, 2, 3]
print(nums[0])
```

---

## 🗺 Maps (Dictionaries)

```
m:Map<str, int> = {"a": 1, "b": 2}
print(m["a"])
```

---

## ⚡ Monomorphization

Katlaz compiles generics into concrete implementations:

```
identity<int>(5)
identity<float>(3.14)
```

Becomes:

```
int identity_int(int x)
double identity_float(double x)
```

This ensures:

* 🚀 Zero runtime overhead
* ⚡ Native performance

---

## 💾 SQLite ORM (Optional)

```
db = sqlite_open("test.db")

User.create_table(db)
User.insert(db, 1, "John")

users = User.all(db)

print(users[0].name)
```

---

## ⚙️ Compilation Pipeline

```
.katlaz
   ↓
Parser (Lark)
   ↓
AST
   ↓
Type Checker
   ↓
Code Generator (C)
   ↓
GCC / Clang
   ↓
Native Binary
```

---

## 🧪 Full Example

```
class Box<T>:
    value:T

    start(value:T):
        self.value = value

func main() -> int:
    nums:List<int> = [1,2,3]
    m:Map<str,int> = {"a":1}

    b:Box<int> = Box(10)

    print(nums[0])
    print(m["a"])
    print(b.value)

    return 0
```

---

## ⚠️ Common Errors

### Type mismatch

```
x:int = "hello"
```

---

### Invalid Map

```
m:Map<str,int> = {"a":1, 2:3}
```

---

### Wrong generic usage

```
identity<int>("text")
```

---

## 🔧 Debugging

To inspect generated C code:

* Open `compiler.py`
* Comment out:

```
os.remove(c_file)
```

---

## 📦 Packaging & Distribution

Katlaz can be distributed as:

* PyPI package (`pip install katlaz`)
* GitHub releases
* Precompiled binaries

---

## 🚀 Roadmap

* LLVM backend
* WebAssembly support
* Package manager
* JIT execution

---

## 📄 License

MIT License

---

## 👨‍💻 Contributing

Pull requests are welcome!
Feel free to open issues or suggest features.

---

## ⭐ Final Notes

Katlaz aims to bridge the gap between:

* Python simplicity
* C performance
* Rust-style generics

Build fast. Compile native. Stay simple.

