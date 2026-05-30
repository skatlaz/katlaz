# FILE: katlazapp/cli.py

import sys
import subprocess
from pathlib import Path
import importlib


# =============================
# CREATE PROJECT
# =============================

def create_project(name: str):
    base = Path(name)
    (base / "app").mkdir(parents=True, exist_ok=True)

    # HTML
    (base / "app/app.html").write_text("""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Katlaz App</title>
</head>
<body>

<h1>Katlaz running</h1>
<p id="status">Waiting...</p>

<button onclick="katlaz.call('hello')">Run Backend</button>

<script src="katlaz.js"></script>
<script>
window.addEventListener("notify", e => {
    document.getElementById("status").innerText = e.detail;
});
</script>

</body>
</html>
""", encoding="utf-8")

    # JS
    (base / "app/katlaz.js").write_text("""window.katlaz = {
    call(name, data = {}) {
        const payload = { name, data };

        if (window.webkit?.messageHandlers?.katlaz) {
            window.webkit.messageHandlers.katlaz.postMessage(JSON.stringify(payload));
        } else {
            fetch("/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(res => this._receive(res))
            .catch(err => console.error(err));
        }
    },

    _receive(res) {
        if (!res) return;

        if (res.error) {
            console.error("Backend error:", res.error);
            return;
        }

        if (res.event) {
            window.dispatchEvent(new CustomEvent(res.event, {
                detail: res.data
            }));
        }
    }
};
""", encoding="utf-8")

    # 🔥 C++ FINAL (bridge híbrido correto)
    (base / "app/AppMain.cpp").write_text(r"""
#include <gtk/gtk.h>
#include <webkit2/webkit2.h>
#include <filesystem>
#include <Python.h>

// INIT PYTHON (UMA VEZ)
void init_python() {
    Py_Initialize();
    PyRun_SimpleString("import sys; sys.path.append('.')");
}

// CALL PYTHON
std::string call_python(const char* json)
{
    PyObject *module = PyImport_ImportModule("katlazapp.runtime.bridge");

    std::string result = "{}";

    if (module) {
        PyObject *func = PyObject_GetAttrString(module, "handle");

        if (func && PyCallable_Check(func)) {
            PyObject *args = PyTuple_Pack(1, PyUnicode_FromString(json));
            PyObject *res = PyObject_CallObject(func, args);

            if (res) {
                // 🔥 dict → JSON
                PyObject* json_mod = PyImport_ImportModule("json");
                PyObject* dumps = PyObject_GetAttrString(json_mod, "dumps");

                PyObject* json_str = PyObject_CallFunctionObjArgs(dumps, res, NULL);

                if (json_str && PyUnicode_Check(json_str)) {
                    result = PyUnicode_AsUTF8(json_str);
                }

                Py_XDECREF(json_str);
                Py_XDECREF(dumps);
                Py_XDECREF(json_mod);
            }

            Py_XDECREF(res);
            Py_DECREF(args);
        }

        Py_DECREF(module);
    }

    return result;
}

// JS → PYTHON
static void on_msg(WebKitUserContentManager*, WebKitJavascriptResult* r, gpointer w)
{
    auto view = WEBKIT_WEB_VIEW(w);
    auto v = webkit_javascript_result_get_js_value(r);

    if (jsc_value_is_string(v)) {
        gchar* msg = jsc_value_to_string(v);

        std::string res = call_python(msg);

        std::string js = "window.katlaz._receive(" + res + ");";
        webkit_web_view_run_javascript(view, js.c_str(), NULL, NULL, NULL);

        g_free(msg);
    }
}

// MAIN
int main(int argc, char** argv)
{
    gtk_init(&argc, &argv);

    init_python();

    auto manager = webkit_user_content_manager_new();
    webkit_user_content_manager_register_script_message_handler(manager, "katlaz");

    auto webview = webkit_web_view_new_with_user_content_manager(manager);

    g_signal_connect(manager, "script-message-received::katlaz", G_CALLBACK(on_msg), webview);

    auto win = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_default_size(GTK_WINDOW(win), 900, 600);

    std::filesystem::path p = std::filesystem::canonical(argv[0]).parent_path();
    std::string url = "file://" + (p / "app/app.html").string();

    webkit_web_view_load_uri(WEBKIT_WEB_VIEW(webview), url.c_str());

    gtk_container_add(GTK_CONTAINER(win), webview);

    g_signal_connect(win, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(win);
    gtk_main();

    Py_Finalize();
    return 0;
}
""")

    # KATLZ
    (base / "main.katlaz").write_text("""route hello:
    emit "notify", "Hello funcionando 🔥"
""")

    print(f"✅ Project '{name}' created")


# =============================
# BUILD
# =============================

def build_exe():
    subprocess.run([
        "pyinstaller",
        "--onefile",
        "--add-data", "app:app",
        "main.py"
    ])

def build(file="main.katlaz"):
    from katlazapp.compiler.parser import parse_katlaz
    from katlazapp.compiler.transpiler import transpile

    path = Path(file)
    ast = parse_katlaz(path.read_text())
    py = transpile(ast)

    out = path.with_suffix(".py")
    out.write_text(py)

    print(f"✅ Compiled: {out}")


# =============================
# DESKTOP
# =============================

def desktop():
    print("🖥️ Building desktop...")

    def run(cmd):
        return subprocess.check_output(cmd).decode().split()

    def detect_webkit():
        for v in ["webkit2gtk-4.1", "webkit2gtk-4.0"]:
            try:
                subprocess.run(["pkg-config", "--exists", v], check=True)
                print(f"✅ Using {v}")
                return v
            except:
                continue
        print("❌ WebKitGTK not found")
        sys.exit(1)

    webkit = detect_webkit()

    flags = run(["pkg-config", "--cflags", "--libs", "gtk+-3.0", webkit])

    try:
        pyflags = run(["python3-config", "--embed", "--cflags", "--ldflags"])
    except:
        pyflags = run(["python3-config", "--cflags", "--ldflags"])

    cmd = ["g++", "app/AppMain.cpp", "-o", "katlaz_app"] + flags + pyflags

    subprocess.run(cmd, check=True)

    print("🚀 Running...")
    subprocess.run(["./katlaz_app"])


# =============================
# SERVE
# =============================

def serve():
    import sys
    from pathlib import Path

    from katlazapp.runtime.app import KatlazApp

    base = Path.cwd()
    sys.path.insert(0, str(base))

    if "main" in sys.modules:
        del sys.modules["main"]

    import main  # ✅ agora funciona

    app = KatlazApp()
    app.run()

"""def serve():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import mimetypes, json

    base = Path.cwd()
    app_dir = base / "app"

    sys.path.append(str(base))

    import main
    importlib.reload(main)

    from katlazapp.runtime.bridge import handle

    class H(BaseHTTPRequestHandler):

        def do_GET(self):
            path = app_dir / ("app.html" if self.path == "/" else self.path.strip("/"))

            if not path.exists():
                self.send_response(404)
                self.end_headers()
                return

            mime = mimetypes.guess_type(path)[0] or "text/plain"

            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.end_headers()
            self.wfile.write(path.read_bytes())

        def do_POST(self):
            if self.path == "/api":
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length).decode()

                result = handle(body)
                res = json.dumps(result)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(res.encode())

    print("🌐 http://localhost:3000")
    HTTPServer(("", 3000), H).serve_forever()"""

# =============================
# CLI
# =============================

def main():
    args = sys.argv

    if len(args) < 2:
        print("Commands: create | build | desktop | serve")
        return

    cmd = args[1]

    if cmd == "create":
        create_project(args[2])

    elif cmd == "build":
        build(args[2] if len(args) > 2 else "main.katlaz")

    elif cmd == "desktop":
        desktop()

    elif cmd == "serve":
        serve()

    else:
        print("❌ Unknown command")
