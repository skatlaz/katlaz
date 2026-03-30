import asyncio
import json
import os
from pathlib import Path

from katlazapp.runtime.core import call_route
from katlazapp.runtime.ws import ws_handler


class KatlazApp:

    def __init__(self):
        self.http_port = 3000
        self.ws_port = 8765

        # 📁 diretório base do projeto (onde roda o CLI)
        self.base_dir = Path.cwd()
        self.app_dir = self.base_dir / "app"

    # =============================
    # HTTP HANDLER
    # =============================
    async def handle_http(self, reader, writer):
        request = await reader.read(2048)
        request = request.decode(errors="ignore")

        # pega primeira linha: GET /path HTTP/1.1
        first_line = request.split("\r\n")[0]
        method, path, _ = first_line.split()

        # =============================
        # API
        # =============================
        if path == "/api" and method == "POST":
            body = request.split("\r\n\r\n")[-1]

            try:
                data = json.loads(body)
                name = data.get("name")
                payload = data.get("data") or {}

                response = call_route(name, payload)

            except:
                response = {"error": "Invalid request"}

            return await self.send_json(writer, response)

        # =============================
        # STATIC FILES
        # =============================
        file_path = self.resolve_path(path)

        if file_path.exists() and file_path.is_file():
            return await self.send_file(writer, file_path)

        # =============================
        # FALLBACK → app.html
        # =============================
        index = self.app_dir / "app.html"

        if index.exists():
            return await self.send_file(writer, index)

        return await self.send_json(writer, {"error": "Not found"}, status=404)

    # =============================
    # PATH RESOLVER
    # =============================
    def resolve_path(self, path):
        if path == "/":
            return self.app_dir / "app.html"

        safe_path = path.lstrip("/")
        return self.base_dir / safe_path

    # =============================
    # SEND JSON
    # =============================
    async def send_json(self, writer, data, status=200):
        body = json.dumps(data)

        response = (
            f"HTTP/1.1 {status} OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            + body
        )

        writer.write(response.encode())
        await writer.drain()
        writer.close()

    # =============================
    # SEND FILE
    # =============================
    async def send_file(self, writer, path):
        try:
            with open(path, "rb") as f:
                content = f.read()
        except:
            return await self.send_json(writer, {"error": "File error"}, 500)

        content_type = self.get_content_type(path)

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
        ).encode() + content

        writer.write(response)
        await writer.drain()
        writer.close()

    # =============================
    # MIME TYPES
    # =============================
    def get_content_type(self, path):
        ext = path.suffix

        return {
            ".html": "text/html",
            ".js": "application/javascript",
            ".css": "text/css",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml"
        }.get(ext, "text/plain")

    # =============================
    # START SERVERS
    # =============================
    async def start_servers(self):
        import websockets

        http_server = await asyncio.start_server(
            self.handle_http,
            "0.0.0.0",
            self.http_port
        )

        ws_server = await websockets.serve(
            ws_handler,
            "0.0.0.0",
            self.ws_port
        )

        print(f"🚀 HTTP: http://localhost:{self.http_port}")
        print(f"⚡ WS: ws://localhost:{self.ws_port}")
        print(f"📁 Serving: {self.app_dir}")

        async with http_server, ws_server:
            await asyncio.gather(
                http_server.serve_forever(),
                ws_server.wait_closed()
            )

    # =============================
    # RUN
    # =============================
    def run(self):
        asyncio.run(self.start_servers())
