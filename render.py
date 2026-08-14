#!/usr/bin/env python3
'''Turn apps.json into apps.js and the case-study markup in docs/index.html.'''
from __future__ import annotations
import html
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pad(n: int) -> str:
    return f"{n:02d}"


def kinetic(name: str) -> str:
    parts = []
    for w in html.escape(name).split():
        parts.append('<span class="clip"><span class="word">' + w + '</span></span>')
    return " ".join(parts)


def shipped(iso) -> str:
    if not iso:
        return ""
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return ""
    return "Shipped %s %s %s" % (d.day, d.strftime("%b"), d.year)


def index_html(apps: list[dict]) -> str:
    bits = []
    for i, app in enumerate(apps, 1):
        slug = html.escape(app["slug"])
        name = html.escape(app["name"])
        bits.append(
            '<a href="#%s" data-slug="%s"><span class="n">%s</span>%s</a>'
            % (slug, slug, pad(i), name)
        )
    return "\n      ".join(bits)


def cases_html(apps: list[dict]) -> str:
    out = []
    arrow = chr(8594)
    for i, app in enumerate(apps):
        n = pad(i + 1)
        flip = " flip" if i % 2 else ""
        shown = " in" if i == 0 else ""
        lazy = "eager" if i == 0 else "lazy"
        fetch = ' fetchpriority="high"' if i == 0 else ""
        slug = html.escape(app["slug"])
        job = html.escape(app["job"])
        pages = html.escape(app["pages"])
        repo = html.escape(app["repo"])
        desk = html.escape(app["desktop"])
        phone = html.escape(app["phone"])
        dalt = html.escape(app.get("desktopAlt") or (app["name"] + " on desktop"))
        palt = html.escape(app.get("phoneAlt") or (app["name"] + " on a phone"))
        when = shipped(app.get("shipped"))
        meta = ('\n          <p class="meta">' + html.escape(when) + "</p>") if when else ""
        block = '''<section class="case%s%s" id="%s" data-n="%s">
        <header class="case-head">
          <p class="idx">%s</p>
          <div class="titles">
            <h2>%s</h2>
            <p class="job">%s</p>%s
          </div>
          <div class="actions">
            <a class="btn open" href="%s">Open live <span class="arr" aria-hidden="true">%s</span></a>
            <a class="btn src" href="%s" rel="noopener noreferrer">Source</a>
          </div>
        </header>
        <div class="stills">
          <figure class="desk">
            <img src="%s" alt="%s" width="1600" height="1000" loading="%s"%s decoding="async">
            <figcaption class="cap">Desktop</figcaption>
          </figure>
          <figure class="phone">
            <img src="%s" alt="%s" width="390" height="844" loading="%s" decoding="async">
            <figcaption class="cap">390</figcaption>
          </figure>
        </div>
      </section>''' % (
            flip, shown, slug, n,
            n, kinetic(app["name"]), job, meta,
            pages, arrow, repo,
            desk, dalt, lazy, fetch,
            phone, palt, lazy,
        )
        out.append(block)
    return "\n\n      ".join(out)


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace(
        '<nav class="index" id="index" aria-label="Shipped apps"></nav>',
        '<nav class="index" id="index" aria-label="Shipped apps">\n      '
        + index_html(data)
        + "\n    </nav>",
    )
    src = src.replace(
        '<div id="cases"></div>',
        '<div id="cases">\n      ' + cases_html(data) + "\n    </div>",
    )
    n = pad(len(data))
    src = src.replace(
        '<span class="cue-n" id="shipped-count">03</span>',
        '<span class="cue-n" id="shipped-count">' + n + "</span>",
    )

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(src)
    (docs / "styles.css").write_text((ROOT / "src" / "styles.css").read_text())
    (docs / "script.js").write_text((ROOT / "src" / "script.js").read_text())
    (docs / "favicon.svg").write_text((ROOT / "src" / "favicon.svg").read_text())
    (docs / "apps.js").write_text(js)
    slim = [
        {k: a[k] for k in ("slug", "name", "job", "pages", "repo", "originalPaid", "shipped") if k in a}
        for a in data
    ]
    (docs / "apps.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False) + "\n")
    shots = docs / "shots"
    shots.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "shots", shots, dirs_exist_ok=True)
    (docs / ".nojekyll").touch()
    print("built %d apps -> %s" % (len(data), docs))


if __name__ == "__main__":
    main()
