#!/usr/bin/env python3
"""Checks the site before you upload it. Python standard library only; nothing is changed.

    python tools/check_site.py

It looks for: broken links and missing images or #anchors, pages without a title,
description or single <h1>, images without alt text or size, a sidebar that differs
between pages, notes and projects missing from assets/site-map.js / lists / sitemap.xml,
draft pages that leaked into public lists, and leftover placeholders on public pages.
Errors make it exit with status 1; warnings are advice only.
"""
import html.parser
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://get2abhijit.github.io/abhijitdeshpande-website/"
errors, warnings = [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.ids, self.links, self.assets, self.imgs = set(), [], [], []
        self.h1 = 0
        self.has_mark = False
        self.lang = None
        self._in_title = False
        self.todo = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "mark":
            self.has_mark = True
        elif tag == "a" and "href" in a:
            self.links.append((a["href"], a.get("target"), a.get("rel", "")))
        elif tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "preload"):
            self.assets.append(a["href"])
        elif tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        elif tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.assets.append(a["src"])
        if "todo" in (a.get("class") or "").split():
            self.todo = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def local_target(base_file, ref):
    """Map a link to a file inside the site, or None if it is external."""
    if ref.startswith(BASE):
        ref = ref[len(BASE):] or "index.html"
        return (ROOT / ref.split("#")[0].split("?")[0]).resolve(), ref.partition("#")[2]
    if re.match(r"^(https?:|mailto:|tel:|data:|//)", ref):
        return None
    path, _, frag = ref.partition("#")
    path = path.split("?")[0]
    if not path:
        return base_file, frag
    target = (base_file.parent / path).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, frag


pages = {}
for f in sorted(ROOT.rglob("*.html")):
    if ".git" in f.parts:
        continue
    p = Page()
    p.feed(f.read_text(encoding="utf-8"))
    pages[f.resolve()] = p

rel = lambda f: f.relative_to(ROOT).as_posix()

# ---- per-page checks -----------------------------------------------------------------
for f, p in pages.items():
    name = rel(f)
    if not p.title.strip():
        err(name, "missing <title>")
    if p.lang is None:
        err(name, "missing lang attribute on <html>")
    if not p.meta.get("description"):
        err(name, "missing meta description")
    if p.h1 != 1:
        err(name, f"expected exactly one <h1>, found {p.h1}")
    for img in p.imgs:
        if "alt" not in img:
            err(name, f"image without alt text: {img.get('src')}")
        if not (img.get("width") and img.get("height")):
            warn(name, f"image without width/height: {img.get('src')}")
    for href, target, relattr in p.links:
        if target == "_blank" and "noopener" not in relattr:
            warn(name, f"external link without rel=noopener: {href}")
        t = local_target(f, href)
        if t is None:
            continue
        tf, frag = t
        if not tf.exists():
            err(name, f"broken link: {href}")
        elif frag and tf.resolve() in pages and frag not in pages[tf.resolve()].ids:
            err(name, f"link to missing anchor: {href}")
    for ref in p.assets:
        t = local_target(f, ref)
        if t and not t[0].exists():
            err(name, f"missing file: {ref}")

# ---- sidebar must match on every page ------------------------------------------------
def sidebar_signature(f):
    text = f.read_text(encoding="utf-8")
    m = re.search(r'<aside class="sidebar".*?</aside>', text, re.S)
    if not m:
        return None
    s = m.group(0)
    s = re.sub(r' aria-current="[^"]*"', "", s)
    s = re.sub(r' class="active-section"', "", s)
    s = re.sub(r'\s*<div data-subnav="[a-z]+"></div>', "", s)
    s = s.replace(BASE, "")
    s = re.sub(r'(href|src)="(?:\.\./)+', r'\1="', s)
    return re.sub(r"\s+", " ", s)


sigs = {rel(f): sidebar_signature(f) for f in pages}
reference = next((s for s in sigs.values() if s), None)
for name, s in sigs.items():
    if s is None:
        err(name, "no sidebar found")
    elif s != reference:
        err(name, "sidebar differs from the other pages (change it the same way everywhere)")

# ---- site map, lists, sitemap, feed -------------------------------------------------
site_map = (ROOT / "assets/site-map.js").read_text(encoding="utf-8")
mapped = re.findall(r"href: '([^']+)'", site_map)
for href in mapped:
    if not (ROOT / href).exists():
        err("assets/site-map.js", f"lists a page that does not exist: {href}")
sitemap_xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
feed_xml = (ROOT / "feed.xml").read_text(encoding="utf-8")
notes_html = (ROOT / "notes.html").read_text(encoding="utf-8")
projects_html = (ROOT / "projects.html").read_text(encoding="utf-8")

for f, p in pages.items():
    name = rel(f)
    parts = pathlib.PurePosixPath(name).parts
    is_note = parts[0] == "notes" and not parts[-1].startswith("_")
    is_project = parts[0] == "projects" or name == "household-finance-tracker.html"
    noindex = "noindex" in p.meta.get("robots", "")
    if is_note or is_project:
        listed = [name in mapped, name in notes_html or name in projects_html, BASE + name in sitemap_xml]
        if noindex:
            if any(listed) or name in feed_xml:
                err(name, "is a draft (noindex) but appears in site-map.js, a list, sitemap.xml or feed.xml")
        else:
            if not listed[0]:
                err(name, "not listed in assets/site-map.js")
            if not listed[1]:
                err(name, "not listed in notes.html / projects.html")
            if not listed[2]:
                err(name, "missing from sitemap.xml")
            if is_note and BASE + name not in feed_xml:
                warn(name, "not in feed.xml")
    if is_note and noindex and not p.meta.get("note-group"):
        warn(name, 'draft has no <meta name="note-group"> (previews will assume "travel")')
    if name != "404.html" and not name.startswith("notes/_") and not noindex:
        if p.has_mark or p.todo:
            err(name, "public page still contains draft highlighting (<mark> or class=todo)")
        text = (ROOT / name).read_text(encoding="utf-8")
        if re.search(r"\[(?:[A-Z][A-Za-z]+ ?)+\]|TODO|Lorem ipsum", re.sub(r"<script.*?</script>|<code>.*?</code>|<pre>.*?</pre>", "", text, flags=re.S)):
            err(name, "looks like it contains a placeholder such as [LinkedIn URL] or TODO")

# ---- big images ---------------------------------------------------------------------
for img in (ROOT / "assets/images").rglob("*"):
    if img.is_file() and img.stat().st_size > 400_000:
        warn(rel(img), f"image is {img.stat().st_size // 1024} KB; consider resizing")

print(f"Checked {len(pages)} pages.")
for w in warnings:
    print("warning:", w)
for e in errors:
    print("ERROR:  ", e)
print(f"{len(errors)} error(s), {len(warnings)} warning(s).")
sys.exit(1 if errors else 0)
