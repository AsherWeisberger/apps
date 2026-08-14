#!/usr/bin/env python3
"""Turn apps.json into apps.js and the case-study markup in docs/index.html."""
from __future__ import annotations

import html
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pad(n: int) -> str:
    return f"{n:02d}"


def shipped(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        return ""
    return f"Shipped {d.day} {d.strftime('%b')} {d.year}"


def index_html(apps: list[dict]) -> str:
    bits = []
    for i, app in enumerate(apps, 1):
        slug = html.escape(app["slug"])
        name = html.escape(app["name"])
        bits.append(
            f'<a href="#{slug}" data-slug="{slug}"><span class="n">{pad(i)}</span>{name}</a>'
        )
    return "\n      ".join(bits)


def cases_html(apps: list[dict]) -> str:
    out = []
    for i, app in enumerate(apps):
        n = pad(i + 1)
        flip = " flip" if i % 2 else ""
        lazy = "eager" if i == 0 else "lazy"
        fetch = ' fetchpriority="high"' if i == 0 else ""
        slug = html.escape(app["slug"])
        name = html.escape(app["name"])
        job = html.escape(app["job"])
        pages = html.escape(app["pages"])
        repo = html.escape(app["repo"])
        desk = html.escape(app["desktop"])
        phone = html.escape(app["phone"])
        dalt = html.escape(app.get("desktopAlt") or f"{app['name']} on desktop")
        palt = html.escape(app.get("phoneAlt") or f"{app['name']} on a phone")
        kname = " ".join(
            f'<span class="clip"><span class="word">{w}</span></span>' for w in name.split()
        )
        when = shipped(app.get("shipped"))
        meta = f'\n          <p class="meta">{html.escape(when)}</p>' if when else ""
        out.append(
            f'''<section class="case{flip}" id="{slug}" data-n="{n}">
        <header class="case-head">
          <p class="idx">{n}</p>
          <div class="titles">
            <h2>{kname}</h2>
            <p class="job">{job}</p>{meta}
          </div>
          <div class="actions">
            <a class="btn open" href="{pages}">Open live <span class="arr" aria-hidden="true">→</span></a>
            <a class="btn src" href="{repo}" rel="noopener noreferrer">Source</a>
          </div>
        </header>
        <div class="stills">
          <figure class="desk">
            <img src="{desk}" alt="{dalt}" width="1600" height="1000" loading="{lazy}"{fetch} decoding="async">
            <figcaption class="cap">Desktop</figcaption>
          </figure>
          <figure class="phone">
            <img src="{phone}" alt="{palt}" width="390" height="844" loading="{lazy}" decoding="async">
            <figcaption class="cap">390</figcaption>
          </figure>
        </div>
      </section>'''
        )
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

    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "index.html").write_text(src)
    (docs / "styles.css").write_text((ROOT / "src" / "styles.css").read_text())
    (docs / "script.js").write_text((ROOT / "src" / "script.js").read_text())
    (docs / "favicon.svg").write_text((ROOT / "src" / "favicon.svg").read_text())
    (docs / "apps.js").write_text(js)
    slim = [
        {
            k: a[k]
            for k in ("slug", "name", "job", "pages", "repo", "originalPaid", "shipped")
            if k in a
        }
        for a in data
    ]
    (docs / "apps.json").write_text(json.dumps(slim, indent=2, ensure_ascii=False) + "\n")
    shots = docs / "shots"
    shots.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "shots", shots, dirs_exist_ok=True)
    (docs / ".nojekyll").touch()
    print(f"built {len(data)} apps → {docs}")


if __name__ == "__main__":
    main()
