# katlaz.pyx
import os
import sys

def create_project(str name):
    base = name

    dirs = [
        "app",
        "pcl",
        "db",
        "api",
        "server",
        "config"
    ]

    os.makedirs(base, exist_ok=True)

    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    readme = f"# {name}\n\nProject create with Katlaz++\n"
    with open(os.path.join(base, "README.md"), "w") as f:
        f.write(readme)

    # HTML básico
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Katlaz App</title>
</head>
<body>
    <h1>Katlaz++ works 🚀</h1>
</body>
</html>
"""
    with open(os.path.join(base, "app", "app.html"), "w") as f:
        f.write(html)

    # C++ GTK WebView
    cpp = f"""
#include <gtk/gtk.h>
#include <webkit2/webkit2.h>

int main(int argc, char *argv[]) {{
    gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "{name}");
    gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);

    GtkWidget *webview = webkit_web_view_new();

    webkit_web_view_load_uri(WEBKIT_WEB_VIEW(webview), "file://app/app.html");

    gtk_container_add(GTK_CONTAINER(window), webview);

    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_widget_show_all(window);
    gtk_main();

    return 0;
}}
"""
    with open(os.path.join(base, "app", "AppMain.cpp"), "w") as f:
        f.write(cpp)

    # Makefile
    makefile = f"""
APP={name}

all:
\tg++ app/AppMain.cpp -o $(APP) `pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.0`

run:
\t./$(APP)
"""
    with open(os.path.join(base, "Makefile"), "w") as f:
        f.write(makefile)

    print(f"Project '{{name}}' created success!")

def release(str name):
    import os
    import subprocess
    import shutil

    base = os.getcwd()
    dist = os.path.join(base, "dist")

    print("🔨 Compiling project...")

    # compilar via MSYS2
    subprocess.run([
        "C:\\msys64\\usr\\bin\\bash.exe",
        "-lc",
        f"cd $(cygpath '{base}') && g++ app/AppMain.cpp -o {name}.exe `pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.0`"
    ])

    if not os.path.exists(f"{name}.exe"):
        print("❌ Fail compiling")
        return

    print("📦 Creating path dist...")
    os.makedirs(dist, exist_ok=True)

    shutil.copy(f"{name}.exe", dist)

    print("🔍 Collecting DLLs...")

    result = subprocess.run([
        "C:\\msys64\\usr\\bin\\bash.exe",
        "-lc",
        f"cd $(cygpath '{base}') && ldd {name}.exe"
    ], capture_output=True, text=True)

    lines = result.stdout.splitlines()

    dlls = []
    for line in lines:
        if "mingw64" in line:
            parts = line.split("=>")
            if len(parts) > 1:
                path = parts[1].strip().split(" ")[0]
                dlls.append(path)

    for dll in dlls:
        try:
            shutil.copy(dll, dist)
        except:
            pass

    shutil.copytree("app", os.path.join(dist, "app"), dirs_exist_ok=True)

    print("✅ Build release success!")
    print(f"📁 Path: {dist}")

def serve():
    import http.server
    import socketserver
    import os

    PORT = 3000
    APP_DIR = os.path.join(os.getcwd(), "app")

    if not os.path.exists(APP_DIR):
        print("❌ Path app/ not found")
        return

    os.chdir(APP_DIR)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.path = "/app.html"
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Katlaz server running on http://localhost:{PORT}")
        print("📁 Server path /app")
        print("⛔ CTRL+C to stop")
        httpd.serve_forever()

def main():
    import sys
    import os

    if len(sys.argv) < 2:
        print("Use: katlaz <command>")
        return

    command = sys.argv[1]

    if command == "create":
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
        print("Command Unknow!")
