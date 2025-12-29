from __future__ import annotations

import argparse
import importlib.resources as resources
import json
import random
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .generator import generate


def _load_index_html() -> bytes:
    return resources.files("seedworld.webui").joinpath("index.html").read_bytes()


class _Handler(BaseHTTPRequestHandler):
    server_version = "seedworld-web/0.1"

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _read_json_body(self) -> dict[str, Any] | None:
        length_raw = self.headers.get("Content-Length")
        if not length_raw:
            return None
        try:
            length = int(length_raw)
        except ValueError:
            return None

        raw = self.rfile.read(length)
        if not raw:
            return None

        try:
            parsed = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None
        return parsed

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/" or self.path.startswith("/?"):
            html = _load_index_html()
            self._send_bytes(HTTPStatus.OK, html, "text/html; charset=utf-8")
            return

        if self.path == "/api/random-seed":
            self._send_json(HTTPStatus.OK, {"seed": random.randint(1, 999_999)})
            return

        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/generate":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        body = self._read_json_body() or {}
        seed_raw = body.get("seed")

        if seed_raw is None or seed_raw == "":
            seed = random.randint(1, 999_999)
        else:
            try:
                seed = int(seed_raw)
            except (TypeError, ValueError):
                self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Seed must be an integer"})
                return

        try:
            spec = generate(seed)
        except Exception as exc:  # noqa: BLE001
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            return

        self._send_json(HTTPStatus.OK, spec.to_dict())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SeedWorld web interface")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), _Handler)

    print(f"SeedWorld web UI running on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
