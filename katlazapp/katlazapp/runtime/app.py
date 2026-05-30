from __future__ import annotations

import asyncio
import json
import mimetypes
from pathlib import Path
from urllib.parse import unquote

from katlazapp.runtime.bridge import handle
from katlazapp.runtime.ws import ws_handler


class KatlazApp:
    def __init__(self, base_dir: str | Path | None = None, http_port: int = 3000, ws_port: int = 8765):
        self.http_port = http_port
        self.ws_port = ws_port
        self.base_dir = Path(base_dir or Path.cwd()).resolve()
        self.app_dir = self.base_dir / "app"

    async def handle_http(self, reader, writer):
        try:
            raw = await reader.read(1024 * 1024)
            request = raw.decode("utf-8", errors="ignore")
            if not request.strip():
                return await self.send_json(writer, {"error": "Empty request"}, 400)
            head, _, body = request.partition("\r\n\r\n")
            first_line = head.split("\r\n", 1)[0]
            parts = first_line.split()
            if len(parts) < 3:
                return await self.send_json(writer, {"error": "Bad request"}, 400)
            method, path, _ = parts

            if path.startswith("/api") and method.upper() == "POST":
                return await self.send_json(writer, handle(body))

            file_path = self.resolve_path(path)
            if file_path.exists() and file_path.is_file():
                return await self.send_file(writer, file_path)

            index = self.app_dir / "app.html"
            if index.exists():
                return await self.send_file(writer, index)
            return await self.send_json(writer, {"error": "Not found"}, 404)
        except Exception as exc:
            return await self.send_json(writer, {"error": str(exc)}, 500)

    def resolve_path(self, path: str) -> Path:
        clean = unquote(path.split("?", 1)[0]).lstrip("/")
        if not clean:
            clean = "app.html"
        candidate = (self.app_dir / clean).resolve()
        # security: only serve files below app/
        if not str(candidate).startswith(str(self.app_dir.resolve())):
            return self.app_dir / "app.html"
        return candidate

    async def send_json(self, writer, data, status=200):
        reason = {200: "OK", 400: "Bad Request", 404: "Not Found", 500: "Internal Server Error"}.get(status, "OK")
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        response = (
            f"HTTP/1.1 {status} {reason}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8") + body
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def send_file(self, writer, path: Path):
        try:
            content = path.read_bytes()
        except Exception:
            return await self.send_json(writer, {"error": "File error"}, 500)
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode("utf-8") + content
        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def start_servers(self):
        import websockets
        http_server = await asyncio.start_server(self.handle_http, "127.0.0.1", self.http_port)
        ws_server = await websockets.serve(ws_handler, "127.0.0.1", self.ws_port)
        print(f"🚀 HTTP: http://localhost:{self.http_port}")
        print(f"⚡ WS: ws://localhost:{self.ws_port}")
        print(f"📁 Serving: {self.app_dir}")
        async with http_server, ws_server:
            await asyncio.gather(http_server.serve_forever(), ws_server.wait_closed())

    def run(self):
        asyncio.run(self.start_servers())
