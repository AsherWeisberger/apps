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


GROUPS = [("All tools", "grid"), ("PDF & documents", "file"), ("Images", "image"), ("Design", "palette"), ("Video & audio", "video"), ("Text & code", "code")]
ICONS = json.loads((ROOT / "src" / "icons.json").read_text())


def category_html(data: list[dict]) -> str:
    groups = GROUPS + [(c, "grid") for c in dict.fromkeys(a.get("category", "Other tools") for a in data) if c not in dict(GROUPS)]
    result = []
    for category, symbol in groups:
        count = len(data) if category == "All tools" else sum(a.get("category", "Other tools") == category for a in data)
        if not count:
            continue
        name = html.escape(category)
        selected = category == "All tools"
        result.append(f'<button type="button" class="category{" selected" if selected else ""}" data-category="{name}" aria-pressed="{str(selected).lower()}">{ICONS[symbol]}<span>{name}</span><span class="category-count">{count}</span></button>')
    return "".join(result)


def card_html(app: dict, i: int) -> str:
    e = html.escape
    slug, name, pages, repo = [e(app[k]) for k in ("slug", "name", "pages", "repo")]
    category = app.get("category", "Other tools")
    description = app.get("description") or app.get("job", "")
    symbol = dict(GROUPS).get(category, "grid")
    tone = next((i-1 for i, (c, _) in enumerate(GROUPS) if c == category), 4)
    lazy = "eager" if i < 3 else "lazy"
    search = e(" ".join([app["name"], category, description, app.get("job", ""), app.get("kicker", "")]).lower())
    return f'''<article class="tool-card tone-{tone}" id="{slug}" data-category="{e(category)}" data-search="{search}">
<a href="{pages}" class="preview-link" aria-label="Open {name}"><img src="{e(still_src(app))}" alt="{e(app.get('desktopAlt', app['name']))}" width="1440" height="900" loading="{lazy}" decoding="async"><span class="preview-action">Open tool {ICONS['arrow']}</span></a>
<div class="card-body"><div class="card-heading"><span class="tool-icon">{ICONS[symbol]}</span><div><h3><a href="{pages}">{name}</a></h3><span class="tool-category">{e(category)}</span></div><a class="launch-icon" href="{pages}" aria-label="Open {name}">{ICONS['arrow']}</a></div><p>{e(description)}</p><div class="card-bottom"><a href="{pages}">Open tool {ICONS['right']}</a><a class="source-link" href="{repo}" target="_blank" rel="noopener noreferrer" aria-label="{name} source code">{ICONS['code']}Source</a></div></div></article>'''


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    for app in data:
        if not pack_path(app).exists():
            make_pack(app)
        if not (ROOT / "shots" / app["slug"] / "card.webp").exists():
            make_stills(app)

    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    newest_first = list(reversed(data))
    cards = "\n\n        ".join(card_html(app, i) for i, app in enumerate(newest_first))
    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace("{{CARDS}}", cards).replace("{{CATEGORIES}}", category_html(data)).replace("{{COUNT}}", str(len(data)))

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(src)
    (docs / "styles.css").write_text((ROOT / "src" / "styles.css").read_text())
    (docs / "script.js").write_text((ROOT / "src" / "script.js").read_text())
    (docs / "favicon.svg").write_text((ROOT / "src" / "favicon.svg").read_text())
    (docs / "apps.js").write_text(js)
    slim_keys = ("slug", "name", "job", "kicker", "pages", "repo", "originalPaid", "shipped", "category", "description")
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
