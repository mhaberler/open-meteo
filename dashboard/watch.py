#!/usr/bin/env python3
"""Tail the six ICON ingest logs and serve the phase chart."""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from phases import DB_PATH, JOBS, LOG_DIR, Follower, Store

STATIC = Path(__file__).resolve().parent / "static"
PORT = int(os.environ.get("INGEST_PORT", "8091"))
STORE = Store(DB_PATH)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/phases.json":
            body = __import__("json").dumps(STORE.query()).encode()
            self._send(200, "application/json; charset=utf-8", body)
            return
        if path in ("/ui", "/ui/"):
            self._send(200, "text/html; charset=utf-8", (STATIC / "index.html").read_bytes())
            return
        if path.startswith("/ui/vendor/"):
            name = path.removeprefix("/ui/vendor/")
            file = (STATIC / "vendor" / name).resolve()
            root = (STATIC / "vendor").resolve()
            if file.is_file() and root in file.parents:
                kind = "text/css" if file.suffix == ".css" else "text/javascript"
                self._send(200, kind, file.read_bytes())
                return
        self._send(404, "text/plain; charset=utf-8", b"not found")

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        return


def follow(store: Store, filename: str, model: str, group: str) -> None:
    path = LOG_DIR / filename
    follower = Follower(store, model, group)
    open_run = store.latest_open_run(follower.job)
    if open_run is not None:
        follower.run = open_run
        follower.saw_download = store.has_phase(follower.job, open_run, "process")
    from_end = True
    while True:
        if not path.exists():
            time.sleep(1)
            continue
        with path.open(errors="replace") as handle:
            ino = os.fstat(handle.fileno()).st_ino
            handle.seek(0, os.SEEK_END if from_end else os.SEEK_SET)
            while True:
                line = handle.readline()
                if line:
                    follower.line(line, datetime.now(timezone.utc))
                    continue
                time.sleep(0.5)
                try:
                    st = path.stat()
                except FileNotFoundError:
                    from_end = False
                    break
                if st.st_ino != ino or st.st_size < handle.tell():
                    from_end = False
                    break


def main() -> None:
    STORE.backfill()
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    import threading

    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"serving 127.0.0.1:{PORT} db={DB_PATH}", flush=True)
    threads = []
    for filename, model, group in JOBS:
        thread = threading.Thread(target=follow, args=(STORE, filename, model, group), daemon=True)
        thread.start()
        threads.append(thread)
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
