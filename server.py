"""Tiny stdlib web server for the Catan Fair Board Generator.

Run:  python3 server.py
Then open http://localhost:8000
"""
import contextlib
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# board.py runs a generation (with lots of debug prints) at import time —
# swallow that output.
with contextlib.redirect_stdout(io.StringIO()):
    import board

HERE = Path(__file__).parent
PORT = 8000


def generate_board():
    with contextlib.redirect_stdout(io.StringIO()):
        b = board.Board()
        b.board_generator()

    tiles = [
        {"id": t.tilenum, "type": t.type, "number": t.number}
        for t in b.board
    ]

    # b.ports is the shuffled visual frame: 6 pieces x 5 slots = the 30
    # coastal edges in ring order, starting at tile 6 side 2.
    ports = [slot for piece in b.ports for slot in piece]

    return {"tiles": tiles, "ports": ports}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (HERE / "index.html").read_bytes()
            self._send(200, "text/html; charset=utf-8", body)
        elif self.path == "/generate":
            body = json.dumps(generate_board()).encode()
            self._send(200, "application/json", body)
        else:
            self._send(404, "text/plain", b"not found")

    def _send(self, status, ctype, body):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # keep the console clean


if __name__ == "__main__":
    print(f"Catan board server running at http://localhost:{PORT}")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
