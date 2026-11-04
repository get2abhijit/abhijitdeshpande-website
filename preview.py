#!/usr/bin/env python3
"""Local preview server: shows the site together with its draft notes.

    python preview.py          (then open the address it prints)
    python preview.py 8002     (use another port)

A draft is any page in notes/ that contains <meta name="robots" content="noindex">
(files starting with "_" are ignored). While this script runs, drafts are added to
the Field notes list and to "Recent writing" on the home page, so you can check
their layout in context. Nothing on disk is changed, so the site you upload to
GitHub Pages still hides them. This file is only for your computer.
"""
import html
import http.server
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BADGE = ('<div style="position:fixed;right:12px;bottom:12px;z-index:9999;background:#1f201c;'
         'color:#fff;font:11px/1 monospace;letter-spacing:.06em;padding:8px 10px">'
         'LOCAL PREVIEW · DRAFTS SHOWN</div>')


def find_drafts():
    drafts = []
    for page in sorted((ROOT / "notes").glob("*.html")):
        if page.name.startswith("_"):
            continue
        text = page.read_text(encoding="utf-8")
        if not re.search(r'<meta\s+name="robots"\s+content="noindex"', text):
            continue
        title = re.search(r"<title>(.*?)</title>", text, re.S)
        desc = re.search(r'<meta name="description" content="(.*?)"', text, re.S)
        title = re.sub(r"\s+—\s+Abhijit Deshpande\s*$", "", title.group(1)) if title else page.stem
        drafts.append((page.name, title, desc.group(1) if desc else ""))
    return drafts


def rows(tag):
    out = []
    for name, title, desc in find_drafts():
        out.append(
            '<li class="note-row"><time class="note-date">DRAFT</time><div>'
            f'<{tag}><a href="notes/{html.escape(name)}">{title}</a></{tag}>'
            f"<p>{desc}</p></div>"
            '<span class="note-type">DRAFT</span></li>\n      '
        )
    return "".join(out)


def prepare(path, text):
    tag = {"index.html": "h3", "notes.html": "h2"}.get(path.name)
    if tag:
        text = text.replace('<ul class="note-list">', '<ul class="note-list">\n      ' + rows(tag), 1)
    return text.replace("</body>", BADGE + "</body>", 1)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        url = self.path.split("?")[0].split("#")[0]
        if url.endswith("/") and (ROOT / url.lstrip("/") / "index.html").exists():
            url += "index.html"
        target = (ROOT / url.lstrip("/")).resolve()
        if target.suffix == ".html" and target.is_file() and ROOT in target.parents:
            body = prepare(target, target.read_text(encoding="utf-8")).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    for candidate in range(port, port + 10):
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", candidate), Handler)
            break
        except OSError:
            print(f"Port {candidate} is busy, trying the next one...")
    else:
        sys.exit("No free port found. Try: python preview.py 9000")
    names = ", ".join(d[0] for d in find_drafts()) or "none found"
    print(f"Local preview: http://localhost:{candidate}/")
    print(f"Drafts shown: {names}")
    print("Stop with Ctrl + C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
