# Katlaz++

A lightweight C++ desktop app framework powered by GTK and WebKit, with a built-in CLI inspired by Node.js workflows.

Katlaz++ allows you to quickly scaffold, develop, serve, and build desktop applications using web technologies (HTML, CSS, JS) rendered inside a native GTK WebView.

---

## 🚀 Features

* ⚡ Project scaffolding via CLI
* 🖥️ Native desktop apps using GTK + WebKit
* 🌐 Built-in development server (`katlaz serve`)
* 📦 Windows release builder with automatic dependency bundling
* 🧩 Modular structure (app, api, db, server, etc.)
* 🔧 Cython-powered CLI for performance

---

## 📁 Project Structure

```
my_app/
├── app/            # Frontend (HTML, CSS, JS)
│   ├── AppMain.cpp # Entry point (GTK WebView)
│   └── app.html    # Main HTML file
├── pcl/            # Core libraries (optional)
├── db/             # Database layer
├── api/            # API logic
├── server/         # Backend/server logic
├── config/         # Configuration files
├── dist/           # Production build output
├── build.bat       # Windows build script
├── run.bat         # Run executable
├── Makefile        # Linux build
├── README.md
```

---

## 🛠️ Installation

### Requirements

#### Linux

* `g++`
* `pkg-config`
* GTK 3
* WebKit2GTK

Install dependencies (Debian/Ubuntu):

```
sudo apt install build-essential pkg-config libgtk-3-dev libwebkit2gtk-4.0-dev
```

#### Windows

* MSYS2
* mingw-w64 toolchain
* GTK3 + WebKit2GTK

Install via MSYS2:

```
pacman -S mingw-w64-x86_64-toolchain \
          mingw-w64-x86_64-gtk3 \
          mingw-w64-x86_64-webkit2gtk
```

---

## 📦 Installing Katlaz CLI

```
pip install cython setuptools
python setup.py build_ext --inplace
pip install .
```

---

## 🧪 Usage

### Create a project

```
katlaz create my_app
cd my_app
```

---

### Start development server

```
katlaz serve
```

Open in browser:

```
http://localhost:3000
```

---

### Build (Linux)

```
make
make run
```

---

### Build (Windows)

Double click:

```
build.bat
```

Run:

```
run.bat
```

---

### Production Build (Windows)

```
katlaz build --release
```

Output:

```
dist/
├── my_app.exe
├── *.dll
├── app/
```

Ready for distribution 🎉

---

## 🖥️ How It Works

Katlaz uses:

* GTK for native windowing
* WebKit for rendering web content
* A local HTTP server (optional) for development

Your app runs inside a WebView:

```cpp
webkit_web_view_load_uri(webview, "http://localhost:3000");
```

---

## 🌐 Development Mode

Using `katlaz serve`:

* Serves `/app` directory
* Uses `app.html` as entry point
* Mimics a Node.js static server

---

## 📦 Distribution

The `--release` mode:

* Compiles your app
* Collects all required DLLs
* Bundles everything into `/dist`
* Optionally generates a `.zip`

---

## ⚠️ Limitations

* WebKitGTK builds can be large (~100MB+)
* Windows support depends on MSYS2
* No code signing (may trigger warnings)

---

## 🔮 Roadmap

* 🔥 Hot reload (`katlaz serve --hot`)
* 🌐 Built-in API system (Express-like)
* ⚡ WebSocket support
* 📦 Cross-platform packaging
* 🧠 Replace WebKit with native WebView2 (Windows)

---

## 🤝 Contributing

Pull requests are welcome!

If you want to propose major changes, please open an issue first.

---

## 📄 License

MIT License

---

## 💡 Inspiration

Katlaz++ is inspired by:

* Node.js
* Electron
* Lightweight native frameworks

---

## ❤️ Author

Created to provide a fast, minimal, and powerful alternative to heavy desktop frameworks.

---

## 🚀 Final Thoughts

Katlaz++ bridges the gap between:

* 🌐 Web development
* 🖥️ Native desktop apps

Build fast. Ship lightweight.
