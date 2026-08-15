#!/usr/bin/env python3
"""Turn apps.json into apps.js and the catalog markup in docs/index.html."""
from __future__ import annotations
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pad(n: int) -> str:
    return f"{n:02d}"


def index_html(apps: list[dict]) -> str:
    bits = []
    for i, app in enumerate(apps, 1):
        slug = html.escape(app["slug"])
        name = html.escape(app["name"])
        bits.append(
            '<a href="#%s" data-slug="%s"><span class="n">%s</span> %s</a>'
            % (slug, slug, pad(i), name)
        )
    return "\n          ".join(bits)


def card_html(app: dict, i: int) -> str:
    n = pad(i + 1)
    lazy = "eager" if i < 2 else "lazy"
    fetch = ' fetchpriority="high"' if i == 0 else ""
    slug = html.escape(app["slug"])
    name = html.escape(app["name"])
    job = html.escape(app["job"])
    pages = html.escape(app["pages"])
    repo = html.escape(app["repo"])
    desk = html.escape(app["desktop"])
    phone = html.escape(app["phone"])
    dalt = html.escape(app.get("desktopAlt") or (app["name"] + " on desktop"))
    palt = html.escape(app.get("phoneAlt") or (app["name"] + " on a phone"))
    paid = html.escape("Replaces " + app["originalPaid"]) if app.get("originalPaid") else ""
    arrow = chr(8594)
    return f'''<article class="card" id="{slug}">
          <a class="still-link" href="{pages}">
            <div class="still-well">
              <img class="desk" src="{desk}" alt="{dalt}" width="1600" height="1000" loading="{lazy}"{fetch} decoding="async">
              <img class="phone" src="{phone}" alt="{palt}" width="390" height="844" loading="{lazy}" decoding="async">
            </div>
          </a>
          <div class="card-body">
            <div class="card-top">
              <p class="kicker">{paid}</p>
              <span class="n">{n}</span>
            </div>
            <h2>{name}</h2>
            <p class="job">{job}</p>
            <div class="actions">
              <a class="btn open" href="{pages}">Open <span class="arr" aria-hidden="true">{arrow}</span></a>
              <a class="btn src" href="{repo}" rel="noopener noreferrer">Source</a>
            </div>
          </div>
        </article>'''


def cases_html(apps: list[dict]) -> str:
    return "\n\n        ".join(card_html(app, i) for i, app in enumerate(apps))


def featured_html(app: dict) -> str:
    pages = html.escape(app["pages"])
    desk = html.escape(app["desktop"])
    phone = html.escape(app["phone"])
    dalt = html.escape(app.get("desktopAlt") or (app["name"] + " on desktop"))
    name = html.escape(app["name"])
    arrow = chr(8594)
    return f'''<a class="frame-shot still-link" href="{pages}">
          <div class="still-well">
            <img class="desk" src="{desk}" alt="{dalt}" width="1600" height="1000" loading="eager" fetchpriority="high" decoding="async">
            <img class="phone" src="{phone}" alt="" width="390" height="844" loading="eager" decoding="async">
          </div>
        </a>
        <p class="frame-cap">
          <span class="kicker">Latest</span>
          <span class="frame-name">{name}</span>
          <span class="frame-go">Open {arrow}</span>
        </p>'''


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace(
        '<nav class="index" id="index" aria-label="Shipped apps"></nav>',
        '<nav class="index" id="index" aria-label="Shipped apps">\n          '
        + index_html(data)
        + "\n        </nav>",
    )
    src = src.replace(
        '<aside class="hero-frame" id="featured"></aside>',
        '<aside class="hero-frame" id="featured">\n        '
        + featured_html(data[-1])
        + "\n      </aside>",
    )
    src = src.replace(
        '<div class="grid" id="cases"></div>',
        '<div class="grid" id="cases">\n        ' + cases_html(data) + "\n      </div>",
    )
    n = pad(len(data))
    src = src.replace(
        '<span id="shipped-count">04</span>',
        '<span id="shipped-count">' + n + "</span>",
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
