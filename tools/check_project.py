#!/usr/bin/env python3
"""Offline structural checks for two independent static landing pages."""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []
        self.h1 = 0
        self.title = 0
        self.lang = False
        self.viewport = False
        self.missing_alt = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = bool(a.get("lang"))
        if a.get("id"): self.ids.add(a["id"])
        if tag == "h1": self.h1 += 1
        if tag == "title": self.title += 1
        if tag == "meta" and a.get("name") == "viewport": self.viewport = bool(a.get("content"))
        if tag == "img" and "alt" not in a: self.missing_alt += 1
        prop = {"a": "href", "link": "href", "script": "src", "img": "src"}.get(tag)
        if prop and prop in a: self.refs.append(a[prop])

def inspect(folder):
    errors = []
    page = folder / "index.html"
    if not page.is_file(): return [f"{folder.name}: index.html missing"]
    check = CheckHTML()
    check.feed(page.read_text(encoding="utf-8"))
    if check.h1 != 1: errors.append(f"{folder.name}: expected 1 h1, found {check.h1}")
    if check.title != 1: errors.append(f"{folder.name}: expected 1 title")
    if not check.lang: errors.append(f"{folder.name}: missing lang")
    if not check.viewport: errors.append(f"{folder.name}: missing viewport")
    if check.missing_alt: errors.append(f"{folder.name}: images without alt")
    for href in check.refs:
        if href.startswith("#"):
            if href[1:] not in check.ids: errors.append(f"{folder.name}: missing anchor {href}")
        elif not href.startswith(("http:", "https:", "//", "mailto:", "tel:", "data:")):
            target = (folder / href.split("#")[0].split("?")[0]).resolve()
            if not target.is_relative_to(folder.resolve()) or not target.exists():
                errors.append(f"{folder.name}: broken local ref {href}")
    for name in ("styles.css", "main.js"):
        if not (folder / name).is_file(): errors.append(f"{folder.name}: missing {name}")
    return errors

if __name__ == "__main__":
    failures = []
    for dirname in ("landing-01", "landing-02"):
        failures.extend(inspect(ROOT / dirname))
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print("OK: two sites, anchors, dependencies and semantics.")
