#!/usr/bin/env python3
"""Assemble the deployable site: the built app (app/out) + the landing page (site/) -> dist/. Standard library only.

- copies app/out, then removes what the sneak peek doesn't serve: challenges, the root redirect, Next's 404 pages
- puts the landing page at / (site/index.html + its CSS, fonts, icon) and the static site/404.html as the 404 page
- writes dist/_headers: the security headers from site/_headers, with a Content-Security-Policy whose script-src is
  'self' plus the sha256 of every inline executable <script> in the built pages (no 'unsafe-inline', no 'unsafe-eval');
  /en/* gets X-Robots-Tag noindex; Next's hashed static files are cached as immutable
- fails when a page loads anything from another origin or a _headers line passes Cloudflare's 2,000-character limit

Usage: python3 scripts/assemble.py [app/out] [dist]
"""

from __future__ import annotations

import base64
import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
LINE_LIMIT = 2000
JS_TYPES = {"", "text/javascript", "application/javascript", "module"}

SCRIPT_RE = re.compile(r"<script\b([^>]*)>(.*?)</script>", re.S | re.I)
ATTR_RE = re.compile(r'([a-zA-Z:-]+)\s*=\s*"([^"]*)"')
LOAD_RE = re.compile(r'<(?:script|img|iframe|source|video|audio|embed|object)\b[^>]*\b(?:src|data)="((?:https?:)?//[^"]+)"', re.I)
LINK_RE = re.compile(r"<link\b([^>]*)>", re.I)
# <link> rels that make the browser fetch something; canonical/alternate are only metadata.
LOADING_RELS = {"stylesheet", "preload", "modulepreload", "prefetch", "preconnect", "dns-prefetch", "icon", "manifest", "apple-touch-icon"}


def fail(msg: str) -> None:
    print(f"assemble: {msg}", file=sys.stderr)
    sys.exit(1)


def remove(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "app" / "out"
    dist = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "dist"
    if not (src / "en.html").exists():
        fail(f"{src} doesn't look like a built app (no en.html)")
    remove(dist)
    shutil.copytree(src, dist)

    # Not part of the sneak peek.
    for p in list(dist.glob("en/challenges*")) + [dist / n for n in ("index.html", "index.txt", "404.html", "_headers")]:
        remove(p)
    for p in dist.glob("_not-found*"):
        remove(p)
    if any(dist.rglob("*challenges*")):
        fail(f"challenge files left: {[str(p) for p in dist.rglob('*challenges*')][:5]}")

    # Landing page at / (the app's robots.txt, built in preview mode, wins over the landing one).
    for item in SITE.iterdir():
        if item.name in {"_headers", "robots.txt"}:
            continue
        target = dist / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)

    hashes: set[str] = set()
    for page in sorted(dist.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        loads = LOAD_RE.findall(html)
        for attrs in LINK_RE.findall(html):
            a = dict(ATTR_RE.findall(attrs))
            href = a.get("href", "")
            if set(a.get("rel", "").lower().split()) & LOADING_RELS and re.match(r"(?:https?:)?//", href):
                loads.append(href)
        if loads:
            fail(f"{page.relative_to(dist)} loads from another origin: {loads[:3]}")
        for attrs, body in SCRIPT_RE.findall(html):
            a = dict(ATTR_RE.findall(attrs))
            if "src" in a or a.get("type", "").lower() not in JS_TYPES:
                continue  # external file (covered by 'self') or data block such as application/ld+json
            digest = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()
            hashes.add(f"'sha256-{digest}'")

    base = {}
    block = re.search(r"^/\*\s*\n((?:[ \t]+.+\n?)+)", (SITE / "_headers").read_text(encoding="utf-8"), re.M)
    if not block:
        fail("site/_headers has no '/*' block")
    for line in block.group(1).splitlines():
        name, _, value = line.strip().partition(":")
        base[name.strip()] = value.strip()

    csp = "; ".join([
        "default-src 'none'",
        "script-src 'self' " + " ".join(sorted(hashes)),
        "style-src 'self'",
        "font-src 'self'",
        "img-src 'self' data:",
        "connect-src 'self'",
        "manifest-src 'self'",
        "base-uri 'none'",
        "form-action 'none'",
        "frame-ancestors 'none'",
        "upgrade-insecure-requests",
    ]).replace("'self' ;", "'self';")
    base["Content-Security-Policy"] = csp

    lines = ["/*"] + [f"  {k}: {v}" for k, v in base.items()]
    lines += ["", "/en", "  X-Robots-Tag: noindex, nofollow", "", "/en/*", "  X-Robots-Tag: noindex, nofollow"]
    lines += ["", "/_next/static/*", "  Cache-Control: public, max-age=31536000, immutable"]
    lines += ["", "/fonts/*", "  Cache-Control: public, max-age=31536000, immutable", ""]
    for line in lines:
        if len(line) > LINE_LIMIT:
            fail(f"_headers line is {len(line)} chars (limit {LINE_LIMIT}): too many inline scripts for one CSP")
    (dist / "_headers").write_text("\n".join(lines), encoding="utf-8")

    pages = len(list(dist.rglob("*.html")))
    print(f"assemble: {pages} pages, {len(hashes)} inline script hashes, CSP {len(csp)} chars -> {dist}")


if __name__ == "__main__":
    main()
