#!/usr/bin/env python3
"""Serve dist/ like Cloudflare Pages does, for the e2e tests: clean URLs (/a -> a.html, /a/ -> a.html or
a/index.html), 404.html with status 404, and the headers from dist/_headers (so the CSP is enforced). Stdlib only.

Usage: python3 scripts/serve.py [dist] [port]     (binds 127.0.0.1)
"""

from __future__ import annotations

import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


def parse_headers(path: Path) -> list[tuple[re.Pattern[str], list[tuple[str, str]]]]:
    rules: list[tuple[re.Pattern[str], list[tuple[str, str]]]] = []
    current: list[tuple[str, str]] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw[0].isspace():
            pattern = "^" + re.escape(raw.strip()).replace(r"\*", ".*") + "$"
            current = []
            rules.append((re.compile(pattern), current))
        elif current is not None:
            name, _, value = raw.strip().partition(":")
            if name.strip().lower() == "content-security-policy":
                # The test server is plain http on 127.0.0.1; this directive would upgrade every subresource to https.
                value = value.replace("; upgrade-insecure-requests", "")
            current.append((name.strip(), value.strip()))
    return rules


class PagesHandler(SimpleHTTPRequestHandler):
    rules: list = []

    def resolve(self, url_path: str) -> Path | None:
        root = os.path.realpath(self.directory)
        rel = unquote(url_path).split("?", 1)[0].strip("/")
        names = ["index.html"] if rel == "" else [rel, f"{rel}.html", os.path.join(rel, "index.html")]
        for name in names:
            # Normalise first, then require the result to stay inside the served directory.
            full = os.path.realpath(os.path.normpath(os.path.join(root, name)))
            if not full.startswith(root + os.sep):
                continue
            if os.path.isfile(full):
                return Path(full)
        return None

    def send_rule_headers(self, url_path: str) -> None:
        for pattern, headers in self.rules:
            if pattern.match(url_path):
                for name, value in headers:
                    self.send_header(name, value)

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET(head=True)

    def do_GET(self, head: bool = False) -> None:  # noqa: N802
        url_path = urlsplit(self.path).path
        target = self.resolve(url_path)
        status = 200
        if target is None:
            target, status = Path(self.directory) / "404.html", 404
            print(f"404 {url_path}", flush=True)
        body = target.read_bytes()
        self.send_response(status)
        self.send_header("Content-Type", self.guess_type(str(target)))
        self.send_header("Content-Length", str(len(body)))
        self.send_rule_headers(url_path)
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def log_message(self, *args) -> None:
        pass


def main() -> None:
    dist = Path(sys.argv[1] if len(sys.argv) > 1 else "dist").resolve()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4173
    PagesHandler.rules = parse_headers(dist / "_headers")
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(PagesHandler, directory=str(dist)))
    print(f"serving {dist} on http://127.0.0.1:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
