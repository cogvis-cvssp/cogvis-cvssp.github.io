#!/usr/bin/env python3
"""Consistency checks for publications.html and the paper pages.

Fails (exit 1) if:
  * a paper folder (papers/<slug>/, BackTranslation2/) has no "Page" button
    in publications.html, or a "Page" button points at a missing folder;
  * publications.html or a paper page has a button link with href="#"
    (other than an explicit "Coming Soon" button).

Standard library only. Usage: python3 scripts/check_publications.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE_DIRS = {"test"}  # scratch pages that should not be listed
errors = []


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def dead_buttons(path):
    for m in re.finditer(r'<a href="#"[^>]*>(.*?)</a>', read(path), re.S):
        label = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if "coming soon" not in label.lower():
            errors.append(f'{path}: dead button href="#" ({label!r})')


pubs = read("publications.html")
linked = set(re.findall(r'href="([^"]+?)/"[^>]*>\s*<i class="fa-solid fa-globe"', pubs))

folders = {"BackTranslation2"}
papers_dir = os.path.join(ROOT, "papers")
for d in sorted(os.listdir(papers_dir)):
    if d not in IGNORE_DIRS and os.path.isfile(os.path.join(papers_dir, d, "index.html")):
        folders.add(f"papers/{d}")

for f in sorted(folders - linked):
    errors.append(f'publications.html: no "Page" button for {f}/')
for f in sorted(linked - folders):
    if not os.path.isfile(os.path.join(ROOT, f, "index.html")):
        errors.append(f'publications.html: "Page" button points at missing {f}/')

for path in ["publications.html"] + [f"{f}/index.html" for f in sorted(folders)]:
    dead_buttons(path)

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("publications OK")
