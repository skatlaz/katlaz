# katlaz.pyx (fixed & organized)
import os
import sys
from pathlib import Path

# =============================
# PROJECT CREATION
# =============================

def create_project(name: str):
    base = name

    dirs = ["app", "pcl", "db", "api", "server", "config"]

    os.makedirs(base, exist_ok=True)

    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # =============================
    # README
    # =============================
    with open(os.path.join(base, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {name}\nKatlaz Desktop App\n")

    # =============================
    # HTML + JS BRIDGE
    # =============================
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Katlaz App</title>
</head>
<body>
    <h1>Katlaz Desktop Running 🚀</h1>

    <button onclick="katlaz.call('hello', {msg: 'Oi'})">
        Testar Bridge
    </button>

    <script>
    window.katlaz = {
        call: function(name, data) {
            const payload = JSON.stringify({ name, data });
            window.webkit.messageHandlers.katlaz.postMessage(payload);
        }
    };
    </script>
</body>
</html>
"""
    with open(os.path.join(base, "app", "app.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # =============================
    # C++ RUNTIME GTK (MULTIPLATAFORMA)
    # =============================
    cpp = f"""
// FILE: app/AppMain.cpp

#include <gtk/gtk.h>
#include <webkit2/webkit2.h>
#include <iostream>
#include <Python.h>

// =============================
// CALL PYTHON BRIDGE
// =============================
void call_python(const char* json)
{{
    Py_Initialize();

    PyObject *pName = PyUnicode_FromString("runtime.bridge");
    PyObject *pModule = PyImport_Import(pName);

    if (pModule != NULL) {{
        PyObject *pFunc = PyObject_GetAttrString(pModule, "handle");

        if (pFunc && PyCallable_Check(pFunc)) {{
            PyObject *args = PyTuple_Pack(1, PyUnicode_FromString(json));
            PyObject *result = PyObject_CallObject(pFunc, args);

            if (result) {{
                std::cout << "Python Response OK" << std::endl;
            }}

            Py_DECREF(args);
        }}
    }}

    Py_Finalize();
}}

// =============================
// JS → C++ → PYTHON
// =============================
static void on_message_received(WebKitUserContentManager *manager,
                                WebKitJavascriptResult *result,
                                gpointer user_data)
{{
    JSCValue *value = webkit_javascript_result_get_js_value(result);

    if (jsc_value_is_string(value)) {{
        gchar *message = jsc_value_to_string(value);

        std::cout << "JS Payload: " << message << std::endl;

        call_python(message);

        g_free(message);
    }}
}}

int main(int argc, char *argv[])
{{
    gtk_init(&argc, &argv);

    WebKitUserContentManager *manager = webkit_user_content_manager_new();

    webkit_user_content_manager_register_script_message_handler(manager, "katlaz");

    g_signal_connect(manager, "script-message-received::katlaz",
                     G_CALLBACK(on_message_received), NULL);

    GtkWidget *webview = webkit_web_view_new_with_user_content_manager(manager);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "{name}");
    gtk_window_set_default_size(GTK_WINDOW(window), 900, 600);

    gtk_container_add(GTK_CONTAINER(window), webview);

    webkit_web_view_load_uri(WEBKIT_WEB_VIEW(webview), "file://app/app.html");

    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(window);
    gtk_main();

    return 0;
}}
"""
    with open(os.path.join(base, "app", "AppMain.cpp"), "w", encoding="utf-8") as f:
        f.write(cpp)

    # =============================
    # MAKEFILE (LINUX / MAC)
    # =============================
    makefile = f"""
# FILE: Makefile

APP={name}

all:
\tg++ app/AppMain.cpp -o $(APP) `pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.0` -lpython3.10

run:
\t./$(APP)
"""
    with open(os.path.join(base, "Makefile"), "w", encoding="utf-8") as f:
        f.write(makefile)

    # =============================
    # WINDOWS BUILD (MSYS2)
    # =============================
    build_win = f"""
:: FILE: build_windows.bat

g++ app/AppMain.cpp -o {name}.exe ^
 -IC:\\msys64\\mingw64\\include ^
 -LC:\\msys64\\mingw64\\lib ^
 -lgtk-3 -lwebkit2gtk-4.0 -lpython3

pause
"""
    with open(os.path.join(base, "build_windows.bat"), "w", encoding="utf-8") as f:
        f.write(build_win)

    print(f"✅ Katlaz Desktop App '{name}' criado com sucesso!")
    print("👉 Use 'make run' (Linux/Mac) ou build_windows.bat (Windows)")


# =============================
# KATLAZ CONVERTER
# =============================

def katlaz_converter(conteudo: str) -> str:
    """Very simple converter: Katlaz -> Cython (.pyx)"""
    conteudo = conteudo.replace("def ", "cpdef ")
    return conteudo


# =============================
# BUILD / RELEASE SYSTEM
# =============================

def release(name: str):
    base_path = Path(os.getcwd())

    katlaz_files = list(base_path.glob("*.katlaz"))
    modules = []

    if not katlaz_files:
        print("⚠️ No .katlaz files found")
        return

    for file in katlaz_files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        converted = katlaz_converter(content)

        module_name = file.stem
        pyx_path = base_path / f"{module_name}.pyx"

        with open(pyx_path, "w", encoding="utf-8") as f:
            f.write(converted)

        modules.append(module_name)

    generate_setup(modules, base_path)


# =============================
# SETUP GENERATOR
# =============================

def generate_setup(modules, base_path: Path):
    module_paths = [str(base_path / (m + ".pyx")) for m in modules]

    setup_code = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        {module_paths},
        compiler_directives={{"language_level": "3"}}
    )
)
"""

    with open(base_path / "setup.py", "w", encoding="utf-8") as f:
        f.write(setup_code)

    print("✅ setup.py created!")
    print("👉 Run: python setup.py build_ext --inplace")


# =============================
# DEV SERVER
# =============================

def serve():
    import http.server
    import socketserver

    PORT = 3000
    app_dir = os.path.join(os.getcwd(), "app")

    if not os.path.exists(app_dir):
        print("❌ app/ folder not found")
        return

    os.chdir(app_dir)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.path = "/app.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Server running at http://localhost:{PORT}")
        print("📁 Serving /app directory")
        print("⛔ Press CTRL+C to stop")
        httpd.serve_forever()


# =============================
# CLI ENTRYPOINT
# =============================

def main():
    if len(sys.argv) < 2:
        print("Use: katlaz <command>")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("Use: katlaz create <project_name>")
            return
        create_project(sys.argv[2])

    elif command == "build":
        if len(sys.argv) > 2 and sys.argv[2] == "--release":
            name = os.path.basename(os.getcwd())
            release(name)
        else:
            print("Use: katlaz build --release")

    elif command == "serve":
        serve()

    else:
        print("❌ Unknown command")


if __name__ == "__main__":
    main()

