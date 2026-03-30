# 🚀 KatlazApp 2.0 — Complete Framework Manual

KatlazApp 2.0 is a **full-stack framework with its own DSL**, designed to unify backend, frontend, and desktop development into a single workflow.

It combines:

* ⚡ Custom DSL (`.katlaz`)
* 🧠 Python runtime engine
* 🌐 HTTP + WebSocket (real-time)
* 🖥️ Desktop support (WebView bridge)
* 🗄️ SQLite ORM
* 📁 File system API

---

# 📦 Installation

```bash
pip install katlazapp
```

Create and run a project:

```bash
katlazapp create myapp
cd myapp
katlazapp build
katlazapp serve
```

---

# 🧠 Architecture

```text
.katlaz → Parser → AST → Transpiler → Python → Runtime → Frontend
```

---

# 📁 Project Structure

```text
myapp/
 ├── main.katlaz
 ├── main.py          # generated
 └── app/
     ├── app.html
     ├── katlaz.js
     └── assets...
```

---

# 🛣️ KATLAZ DSL — FULL COMMAND REFERENCE

## 🔹 Routes

Define backend endpoints:

```katlaz
route hello:
    emit "notify", "Hello World"
```

With parameters:

```katlaz
route greet(name: string):
    emit "notify", name
```

---

## 🔹 Variables & Expressions

```katlaz
route calc:
    x = 10
    y = x + 5
    emit "result", y
```

---

## 🔹 Emit (Frontend Events)

```katlaz
emit "notify", "Message"
emit "result", 123
```

---

## 🔹 Return Values

```katlaz
route raw:
    return 123
```

---

## 🔹 Type System

Supported types:

* `string`
* `int`
* `float`
* `bool`
* `any`

Example:

```katlaz
route sum(a: int, b: int):
    emit "result", a + b
```

---

## 🔹 Database (SQLite ORM)

### Define Model

```katlaz
model users:
    id int
    name string
```

### Insert

```katlaz
db.insert "users", {name: name}
```

### Select

```katlaz
users = db.select "users"
```

---

## 🔹 File System

### Write

```katlaz
fs.write "file.txt", "Hello"
```

### Read

```katlaz
data = fs.read "file.txt"
```

---

# 🌐 JAVASCRIPT API

## Call Backend

```javascript
katlaz.call("hello")
```

```javascript
katlaz.call("greet", { name: "John" })
```

---

## Receive Events

```javascript
window.addEventListener("notify", e => {
    console.log(e.detail)
})
```

---

## WebSocket Mode (Real-time)

```javascript
const ws = new WebSocket("ws://localhost:8765")

ws.onmessage = (msg) => {
    const res = JSON.parse(msg.data)
    katlaz._receive(res)
}

katlaz.call = (name, data = {}) => {
    ws.send(JSON.stringify({ name, data }))
}
```

---

# 🌐 HTML EXAMPLE

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>

<h1>KatlazApp</h1>
<p id="status">Waiting...</p>

<button onclick="katlaz.call('hello')">Run</button>

<script src="katlaz.js"></script>
<script>
window.addEventListener("notify", e => {
    document.getElementById("status").innerText = e.detail;
});
</script>

</body>
</html>
```

---

# ⚙️ CLI COMMANDS

## Create Project

```bash
katlazapp create myapp
```

## Build (.katlaz → Python)

```bash
katlazapp build
```

## Run Server (HTTP + WS)

```bash
katlazapp serve
```

## Desktop Mode

```bash
katlazapp desktop
```

---

# 🌐 HTTP SERVER

* Runs at: `http://localhost:3000`
* Serves static files automatically
* Loads `app/app.html` by default
* `/api` handles backend routes

---

# ⚡ WEBSOCKET SERVER

* Runs at: `ws://localhost:8765`
* Real-time communication
* No polling

---

# 🔄 FULL FLOW

```text
Frontend → katlaz.call()
          ↓
       HTTP / WS
          ↓
      call_route()
          ↓
      Python runtime
          ↓
        emit()
          ↓
      Frontend event
```

---

# ❌ ERROR SYSTEM

## Type Error

```json
{
  "error": "Invalid type for 'name'",
  "code": "KATLAZ_ERROR",
  "hint": "Expected string"
}
```

---

## Runtime Error

```json
{
  "error": "division by zero",
  "code": "RUNTIME_ERROR"
}
```

---

## Syntax Error

```text
[Katlaz Syntax Error] line 3: emit notify
```

---

# 🧠 FEATURES

* DSL-based backend
* Automatic type validation
* Auto-casting
* SQLite ORM
* File system access
* WebSocket real-time
* Static file server
* SPA support

---

# 🖥️ DESKTOP MODE

* Native WebView
* No HTTP required
* Direct JS ↔ Python communication

---

# 📦 BUILD EXECUTABLE

```bash
pyinstaller --onefile main.py
```

---

# 🔥 DEBUGGING

## Python

```python
print("DEBUG:", data)
```

## JavaScript

```javascript
console.log("Debug")
```

---

# 🔐 SECURITY NOTES

* Validate user input
* Avoid exposing file paths
* Add authentication layer (future)

---

# 🧩 ROADMAP

* Authentication (JWT)
* Middleware system
* Plugin system
* Hot reload
* Type inference
* IDE integration

---

# 🤝 CONTRIBUTING

1. Fork repository
2. Create branch
3. Submit PR

---

# 📄 LICENSE

MIT License

---

# 🚀 FINAL

KatlazApp 2.0 is a **full-stack framework with its own language**, enabling you to build:

* Backend APIs
* Frontend interfaces
* Desktop apps

All in one unified system.

---

🔥 **Welcome to KatlazApp 2.0**
