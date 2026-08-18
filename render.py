#!/usr/bin/env python3
"""Turn apps.json into apps.js and the storefront markup in docs/.

Append one object to apps.json and re-run ./build.sh.
JSON order is oldest → newest. The page shows newest first.
Packshots are square crops of each desktop still (shots/<slug>/pack.png).
An optional "still" field skips pack generation and uses that path instead.
Optional "packAlign": "right" | "left" | "center" (default center).
"""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
PACK_SIZE = 1200


def pack_path(app: dict) -> Path:
    return ROOT / "shots" / app["slug"] / "pack.png"


def still_src(app: dict) -> str:
    if app.get("still"):
        return app["still"]
    return "./shots/%s/pack.png" % app["slug"]


def make_pack(app: dict) -> None:
    if app.get("still"):
        return
    desktop = ROOT / app["desktop"].lstrip("./")
    dest = pack_path(app)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(desktop).convert("RGB")
    w, h = im.size
    side = min(w, h)
    align = (app.get("packAlign") or "center").lower()
    if align == "right":
        left = w - side
    elif align == "left":
        left = 0
    else:
        left = (w - side) // 2
    top = 0 if h >= side else (h - side) // 2
    crop = im.crop((left, top, left + side, top + side))
    crop = crop.resize((PACK_SIZE, PACK_SIZE), Image.Resampling.LANCZOS)
    crop.save(dest, "PNG", optimize=True)


def still_img(app: dict, lazy: str, fetch: str = "") -> str:
    src = html.escape(still_src(app))
    alt = html.escape(app.get("desktopAlt") or app["name"])
    return (
        '<img src="%s" alt="%s" width="1200" height="750" loading="%s"%s decoding="async">'
        % (src, alt, lazy, fetch)
    )


def card_html(app: dict, i: int) -> str:
    lazy = "eager" if i < 2 else "lazy"
    fetch = ' fetchpriority="high"' if i == 0 else ""
    slug = html.escape(app["slug"])
    name = html.escape(app["name"])
    pages = html.escape(app["pages"])
    repo = html.escape(app["repo"])
    job = html.escape(app.get("job") or "")
    kind = html.escape("Original alternative" if app.get("originalPaid") else "Browser utility")
    img = still_img(app, lazy, fetch)
    return (
        '<article class="card reveal" id="%s">\n'
        '          <div class="card-top"><span class="number">0%d</span><span>%s</span></div>\n'
        '          <a class="still" href="%s" aria-label="Open %s">\n'
        "            %s\n"
        "          </a>\n"
        '          <div class="card-info"><div><h2>%s</h2><p class="card-copy">%s</p></div>'
        '<div class="links"><a class="button primary" href="%s">Open app ↗</a>'
        '<a class="button" href="%s" rel="noopener noreferrer">Source</a></div></div>\n'
        "        </article>"
        % (slug, i + 1, kind, pages, name, img, name, job, pages, repo)
    )


def island_html(app: dict) -> str:
    return (
        '<a class="island" id="island" href="%s">Open %s</a>'
        % (html.escape(app["pages"]), html.escape(app["name"]))
    )


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    for app in data:
        make_pack(app)

    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    newest_first = list(reversed(data))
    cards = "\n\n        ".join(card_html(app, i) for i, app in enumerate(newest_first))

    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace(
        '<div class="grid" id="grid"></div>',
        '<div class="grid" id="grid">\n        ' + cards + "\n      </div>",
    )
    src = src.replace(
        '<a class="island" id="island" href="#"></a>',
        island_html(data[-1]),
    )

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(src)
    (docs / "styles.css").write_text((ROOT / "src" / "styles.css").read_text())
    (docs / "script.js").write_text((ROOT / "src" / "script.js").read_text())
    (docs / "favicon.svg").write_text((ROOT / "src" / "favicon.svg").read_text())
    (docs / "apps.js").write_text(js)
    slim_keys = ("slug", "name", "job", "pages", "repo", "originalPaid", "shipped")
    slim = [{k: a[k] for k in slim_keys if k in a} for a in data]
    (docs / "apps.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False) + "\n")

    fonts_src = ROOT / "src" / "fonts"
    fonts_dst = docs / "fonts"
    if fonts_src.exists():
        fonts_dst.mkdir(exist_ok=True)
        for f in fonts_src.iterdir():
            if f.is_file():
                shutil.copy2(f, fonts_dst / f.name)

    shots = docs / "shots"
    shots.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "shots", shots, dirs_exist_ok=True)
    (docs / ".nojekyll").touch()
    print("built %d apps -> %s" % (len(data), docs))


if __name__ == "__main__":
    main()
