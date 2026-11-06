#!/usr/bin/env python3
"""Local preview server: shows the site together with its draft notes.

    python preview.py          (then open the address it prints)
    python preview.py 8002     (use another port)

A draft is any page in notes/ that contains <meta name="robots" content="noindex">
(files starting with "_" are ignored). Its group comes from
<meta name="note-group" content="travel"> (travel, cricket-family or engineering).

While this script runs, drafts are added to the Notes list, to "Recent writing" on the
home page, to the sidebar menu and to previous/next links, so you can check their
layout in context. Nothing on disk is changed, so the site you upload to GitHub Pages
still hides them. This file is only for your computer; you don't need to upload it.
"""
import html
import http.server
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BADGE = ('<div style="position:fixed;right:12px;bottom:12px;z-index:9999;background:#13212a;'
         'color:#fff;font:11px/1 monospace;letter-spacing:.06em;padding:8px 10px;border-radius:4px">'
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
        group = re.search(r'<meta name="note-group" content="(.*?)"', text)
        title = re.sub(r"\s+—\s+Abhijit Deshpande\s*$", "", title.group(1)) if title else page.stem
        drafts.append({"href": f"notes/{page.name}", "title": html.unescape(title),
                       "desc": desc.group(1) if desc else "", "group": group.group(1) if group else "travel"})
    return drafts


def row(d, tag):
    return ('<li class="row note-row draft-row"><div>'
            f'<{tag}><a href="{html.escape(d["href"])}">{html.escape(d["title"])}</a></{tag}>'
            f'<p>{d["desc"]}</p></div><div class="meta">Draft</div></li>')


def prepare_html(path, text):
    drafts = find_drafts()
    if path.name == "index.html":
        i = text.find('<ul class="rows note-list">')
        if i != -1 and drafts:
            i += len('<ul class="rows note-list">')
            text = text[:i] + "".join(row(d, "h3") for d in drafts) + text[i:]
    elif path.name == "notes.html":
        for gid in {d["group"] for d in drafts}:
            start = text.find(f'<section data-group="{gid}"')
            if start == -1:
                continue
            end = text.find(">", start)
            text = text[:start] + text[start:end + 1].replace(" hidden", "") + text[end + 1:]
            j = text.find('<ul class="rows note-list">', start) + len('<ul class="rows note-list">')
            text = text[:j] + "".join(row(d, "h3") for d in drafts if d["group"] == gid) + text[j:]
    return text.replace("</body>", BADGE + "</body>", 1)


def prepare_sitemap_js(text):
    items = [{"href": d["href"], "title": d["title"], "group": d["group"]} for d in find_drafts()]
    return text + f"\nwindow.SITE.notes = {json.dumps(items, ensure_ascii=False)}.concat(window.SITE.notes);\n"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _send(self, body, ctype):
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = self.path.split("?")[0].split("#")[0]
        if url.endswith("/") and (ROOT / url.lstrip("/") / "index.html").exists():
            url += "index.html"
        target = (ROOT / url.lstrip("/")).resolve()
        if target.is_file() and ROOT in target.parents:
            if target.suffix == ".html":
                return self._send(prepare_html(target, target.read_text(encoding="utf-8")), "text/html; charset=utf-8")
            if target.name == "site-map.js":
                return self._send(prepare_sitemap_js(target.read_text(encoding="utf-8")), "text/javascript; charset=utf-8")
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
    names = ", ".join(d["href"].split("/")[-1] for d in find_drafts()) or "none found"
    print(f"Local preview: http://localhost:{candidate}/")
    print(f"Drafts shown: {names}")
    print("Stop with Ctrl + C.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
