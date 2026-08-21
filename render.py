#!/usr/bin/env python3
"""Turn apps.json into apps.js and the storefront markup in docs/.

Append one object to apps.json and re-run ./build.sh.
JSON order is oldest -> newest. The page shows newest first.
Packshots are square crops of each desktop still (shots/<slug>/pack.png).
card.webp / phone.webp are the gallery stills (fast, real UI).
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
CARD_WIDTH = 1440
PHONE_WIDTH = 780


def pack_path(app: dict) -> Path:
    return ROOT / "shots" / app["slug"] / "pack.png"


def still_src(app: dict) -> str:
    if app.get("still"):
        return app["still"]
    return "./shots/%s/card.webp" % app["slug"]


def phone_src(app: dict) -> str:
    return "./shots/%s/phone.webp" % app["slug"]


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


def make_webp(src: Path, dest: Path, max_w: int, quality: int = 78) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w > max_w:
        nh = max(1, int(round(h * max_w / w)))
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "WEBP", quality=quality, method=6)


def make_stills(app: dict) -> None:
    slug = app["slug"]
    desktop = ROOT / app["desktop"].lstrip("./")
    phone = ROOT / app["phone"].lstrip("./")
    folder = ROOT / "shots" / slug
    if desktop.exists() and not app.get("still"):
        make_webp(desktop, folder / "card.webp", CARD_WIDTH, 78)
    if phone.exists():
        make_webp(phone, folder / "phone.webp", PHONE_WIDTH, 78)


def num(i: int) -> str:
    return "%02d" % (i + 1)


def card_html(app: dict, i: int) -> str:
    lazy = "eager" if i < 2 else "lazy"
    fetch = ' fetchpriority="high"' if i == 0 else ""
    slug = html.escape(app["slug"])
    name = html.escape(app["name"])
    pages = html.escape(app["pages"])
    repo = html.escape(app["repo"])
    job = html.escape(app.get("job") or "")
    kicker = html.escape(app.get("kicker") or ("Original alternative" if app.get("originalPaid") else "Browser utility"))
    alt = html.escape(app.get("desktopAlt") or app["name"])
    desk = html.escape(still_src(app))
    phone = html.escape(phone_src(app))
    featured = " featured" if i == 0 else ""
    device = (
        '<img class="device" src="%s" alt="" width="390" height="844" decoding="async">' % phone
        if i == 0
        else ""
    )
    return (
        '<article class="card%s reveal" id="%s">\n'
        '          <a class="still" href="%s" aria-label="Open %s">\n'
        "            <picture>\n"
        '              <source media="(max-width:700px)" srcset="%s">\n'
        '              <img src="%s" alt="%s" width="1440" height="900" loading="%s"%s decoding="async">\n'
        "            </picture>\n"
        "            %s\n"
        '            <span class="open-chip">Open</span>\n'
        "          </a>\n"
        '          <div class="meta">\n'
        '            <div class="card-top"><span class="number">%s</span><span>%s</span></div>\n'
        '            <h2 data-name="%s">%s</h2>\n'
        '            <p class="card-copy">%s</p>\n'
        '            <div class="links">\n'
        '              <a class="btn primary" href="%s">Open<span class="fill" aria-hidden="true"></span></a>\n'
        '              <a class="btn" href="%s" rel="noopener noreferrer">Source<span class="fill" aria-hidden="true"></span></a>\n'
        "            </div>\n"
        "          </div>\n"
        "        </article>"
        % (featured, slug, pages, name, phone, desk, alt, lazy, fetch, device, num(i), kicker, name, name, job, pages, repo)
    )


def chip_html(app: dict, i: int) -> str:
    return (
        '<a href="#%s"><em>%s</em>%s</a>'
        % (html.escape(app["slug"]), num(i), html.escape(app["name"]))
    )


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    for app in data:
        make_pack(app)
        make_stills(app)

    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    newest_first = list(reversed(data))
    cards = "\n\n        ".join(card_html(app, i) for i, app in enumerate(newest_first))
    chips = "".join(chip_html(app, i) for i, app in enumerate(newest_first))

    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace(
        '<div class="shop" id="shop"></div>',
        '<div class="shop" id="shop">\n        ' + cards + "\n      </div>",
    )
    src = src.replace(
        '<div class="chips" id="chips"></div>',
        '<div class="chips" id="chips">' + chips + "</div>",
    )

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(src)
    (docs / "styles.css").write_text((ROOT / "src" / "styles.css").read_text())
    (docs / "script.js").write_text((ROOT / "src" / "script.js").read_text())
    (docs / "favicon.svg").write_text((ROOT / "src" / "favicon.svg").read_text())
    (docs / "apps.js").write_text(js)
    slim_keys = ("slug", "name", "job", "kicker", "pages", "repo", "originalPaid", "shipped")
    slim = [{k: a[k] for k in slim_keys if k in a} for a in data]
    (docs / "apps.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False) + "\n")

    fonts_src = ROOT / "src" / "fonts"
    fonts_dst = docs / "fonts"
    if fonts_src.exists():
        fonts_dst.mkdir(exist_ok=True)
        for f in fonts_src.iterdir():
            if f.is_file():
                shutil.copy2(f, fonts_dst / f.name)

    js_src = ROOT / "src" / "js"
    js_dst = docs / "js"
    if js_src.exists():
        js_dst.mkdir(exist_ok=True)
        for f in js_src.iterdir():
            if f.is_file():
                shutil.copy2(f, js_dst / f.name)

    shots = docs / "shots"
    shots.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "shots", shots, dirs_exist_ok=True)
    (docs / ".nojekyll").touch()
    print("built %d apps -> %s" % (len(data), docs))


if __name__ == "__main__":
    main()
