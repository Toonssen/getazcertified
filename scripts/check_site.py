#!/usr/bin/env python3
"""Checks the static site in site/ before it can be merged (CI job `check`). Standard library only.

- every local reference (href/src in HTML, url() in CSS) points at a file that exists
- nothing is loaded from another origin: no external src, stylesheet, font or url() (plain <a href> links are fine)
- no <script> at all, no inline event handlers, no inline style attributes (the CSP forbids them)
- site/_headers sets the security headers the page relies on
- HTML parses cleanly (balanced tags), has lang, a <title>, a viewport meta and a description

Exit 0 when everything passes, 1 otherwise. Without a site/ folder there is nothing to check (exit 0).
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE = Path(__file__).resolve().parent.parent / "site"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

REQUIRED_HEADERS = {
    "Content-Security-Policy": ["default-src 'none'", "frame-ancestors 'none'"],
    "Strict-Transport-Security": ["max-age="],
    "X-Content-Type-Options": ["nosniff"],
    "Referrer-Policy": ["no-referrer"],
    "Permissions-Policy": [],
    "Cross-Origin-Opener-Policy": ["same-origin"],
}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def is_external(url: str) -> bool:
    p = urlparse(url)
    return bool(p.scheme and p.scheme not in ("", "data")) or url.startswith("//")


def check_local(ref: str, base: Path, where: str) -> None:
    if not ref or ref.startswith(("#", "mailto:")):
        return
    path = urlparse(ref).path
    target = (SITE / path.lstrip("/")) if path.startswith("/") else (base.parent / path)
    if path.endswith("/"):
        target = target / "index.html"
    if not target.resolve().is_relative_to(SITE):
        err(f"{where}: {ref} points outside site/")
    elif not target.exists():
        err(f"{where}: {ref} does not exist")


class Page(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.stack: list[str] = []
        self.seen: dict[str, list[dict[str, str]]] = {}

    def where(self) -> str:
        return f"{self.path.relative_to(SITE.parent)}:{self.getpos()[0]}"

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k: (v or "") for k, v in attrs_list}
        self.seen.setdefault(tag, []).append(attrs)
        if tag == "script":
            err(f"{self.where()}: <script> is not allowed")
        for k in attrs:
            if k.startswith("on"):
                err(f"{self.where()}: inline handler {k}= is not allowed")
            if k == "style":
                err(f"{self.where()}: inline style= is not allowed (CSP style-src 'self')")
        for k in ("src", "srcset", "poster", "data"):
            if k in attrs:
                if is_external(attrs[k]):
                    err(f"{self.where()}: external {k}={attrs[k]}")
                else:
                    check_local(attrs[k], self.path, self.where())
        if "href" in attrs:
            href = attrs["href"]
            if tag == "a":
                if is_external(href) and not href.startswith("https://"):
                    err(f"{self.where()}: link {href} is not https")
                elif not is_external(href):
                    check_local(href, self.path, self.where())
                if attrs.get("target") == "_blank" and "noopener" not in attrs.get("rel", ""):
                    err(f"{self.where()}: target=_blank without rel=noopener")
            elif is_external(href):
                err(f"{self.where()}: external <{tag} href={href}>")
            else:
                check_local(href, self.path, self.where())
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs_list)
        if tag not in VOID and self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            err(f"{self.where()}: unexpected </{tag}> (open: {self.stack[-3:]})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
            return
        self.stack.pop()


def check_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(SITE.parent)
    if not text.lstrip().lower().startswith("<!doctype html>"):
        err(f"{rel}: missing <!doctype html>")
    page = Page(path)
    page.feed(text)
    page.close()
    if page.stack:
        err(f"{rel}: unclosed tags {page.stack}")
    html = page.seen.get("html", [{}])[0]
    if not html.get("lang"):
        err(f"{rel}: <html> has no lang")
    if "title" not in page.seen:
        err(f"{rel}: no <title>")
    metas = page.seen.get("meta", [])
    if not any(m.get("name") == "viewport" for m in metas):
        err(f"{rel}: no viewport meta")
    if not any(m.get("name") == "description" and m.get("content") for m in metas):
        err(f"{rel}: no description meta")
    if not any(m.get("charset", "").lower() == "utf-8" for m in metas):
        err(f"{rel}: no <meta charset=utf-8>")


def check_css(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(SITE.parent)
    if re.search(r"@import", text):
        err(f"{rel}: @import is not allowed")
    for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", text):
        ref = m.group(1)
        line = text.count("\n", 0, m.start()) + 1
        if is_external(ref):
            err(f"{rel}:{line}: external url({ref})")
        else:
            check_local(ref, path, f"{rel}:{line}")


def check_headers() -> None:
    path = SITE / "_headers"
    if not path.exists():
        err("site/_headers is missing")
        return
    text = path.read_text(encoding="utf-8")
    block = re.search(r"^/\*\s*\n((?:[ \t]+.+\n?)+)", text, re.M)
    if not block:
        err("site/_headers has no '/*' block")
        return
    headers: dict[str, str] = {}
    for line in block.group(1).splitlines():
        name, _, value = line.strip().partition(":")
        headers[name.strip()] = value.strip()
    for name, needles in REQUIRED_HEADERS.items():
        if name not in headers:
            err(f"site/_headers: {name} missing for /*")
            continue
        for needle in needles:
            if needle not in headers[name]:
                err(f"site/_headers: {name} lacks {needle!r}")


def main() -> int:
    if not SITE.is_dir():
        print("check_site: no site/ folder, nothing to check")
        return 0
    for p in sorted(SITE.rglob("*.html")):
        check_html(p)
    for p in sorted(SITE.rglob("*.css")):
        check_css(p)
    check_headers()
    for e in errors:
        print(f"ERROR {e}")
    print(f"check_site: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
