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

    # cria diretório base
    os.makedirs(base, exist_ok=True)

    # cria subpastas
    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # README
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


def main():
    import sys
    import os

    if len(sys.argv) < 2:
        print("Use: katlaz <comando>")
        return

    command = sys.argv[1]

    if command == "create":
        create_project(sys.argv[2])

    elif command == "build":
        if len(sys.argv) > 2 and sys.argv[2] == "--release":
            name = os.path.basename(os.getcwd())
            build_release(name)
        else:
            print("Use: katlaz build --release")

    elif command == "serve":
        serve()

    else:
        print("Command Unknow!")
        
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
