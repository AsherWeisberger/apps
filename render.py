#!/usr/bin/env python3
"""Turn apps.json into apps.js and the catalog markup in docs/index.html.

Append one object to apps.json and re-run ./build.sh to add a row.
The last entry is the hero still. Rows alternate still-left / still-right.
An optional "still" field overrides "desktop" for the directed frame.
"""
from __future__ import annotations
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def still_src(app: dict) -> str:
    return app.get("still") or app["desktop"]


def still_img(app: dict, lazy: str, fetch: str = "") -> str:
    src = html.escape(still_src(app))
    alt = html.escape(app.get("desktopAlt") or (app["name"] + " editor"))
    return (
        '<img src="%s" alt="%s" width="1600" height="1000" loading="%s"%s decoding="async">'
        % (src, alt, lazy, fetch)
    )


def row_html(app: dict, i: int) -> str:
    lazy = "eager" if i < 2 else "lazy"
    fetch = ' fetchpriority="high"' if i == 0 else ""
    flip = " is-flip" if i % 2 == 1 else ""
    slug = html.escape(app["slug"])
    name = html.escape(app["name"])
    job = html.escape(app["job"])
    pages = html.escape(app["pages"])
    repo = html.escape(app["repo"])
    paid = html.escape("Replaces " + app["originalPaid"]) if app.get("originalPaid") else ""
    kicker = ('<p class="kicker">%s</p>\n          ' % paid) if paid else ""
    arrow = chr(8594)
    return (
        '<article class="row%s" id="%s" style="--i:%d">\n'
        '        <a class="row-still" href="%s">\n'
        "          <figure>\n"
        "            %s\n"
        "          </figure>\n"
        "        </a>\n"
        '        <div class="row-copy">\n'
        "          %s<h2>%s</h2>\n"
        '          <p class="job">%s</p>\n'
        '          <div class="actions">\n'
        '            <a class="btn open" href="%s">Open <span class="arr" aria-hidden="true">%s</span></a>\n'
        '            <a class="src" href="%s" rel="noopener noreferrer">Source</a>\n'
        "          </div>\n"
        "        </div>\n"
        "      </article>"
        % (flip, slug, i, pages, still_img(app, lazy, fetch), kicker, name, job, pages, arrow, repo)
    )


def cases_html(apps: list[dict]) -> str:
    return "\n\n      ".join(row_html(app, i) for i, app in enumerate(apps))


def featured_html(app: dict) -> str:
    pages = html.escape(app["pages"])
    name = html.escape(app["name"])
    return (
        '<a class="hero-frame" href="%s">\n'
        "          <figure>\n"
        "            %s\n"
        "          </figure>\n"
        '          <p class="hero-cap">\n'
        '            <span class="kicker">Latest</span>\n'
        '            <span class="hero-name">%s</span>\n'
        "          </p>\n"
        "        </a>"
        % (pages, still_img(app, "eager", ' fetchpriority="high"'), name)
    )


def foot_apps_html(apps: list[dict]) -> str:
    bits = []
    for app in apps:
        bits.append(
            '<a href="%s">%s</a>'
            % (html.escape(app["pages"]), html.escape(app["name"]))
        )
    return "\n        ".join(bits)


def main() -> None:
    data = json.loads((ROOT / "apps.json").read_text())
    js = "window.APPS = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"
    (ROOT / "apps.js").write_text(js)

    src = (ROOT / "src" / "index.html").read_text()
    src = src.replace(
        '<aside class="hero-still" id="featured"></aside>',
        '<aside class="hero-still" id="featured">\n        '
        + featured_html(data[-1])
        + "\n      </aside>",
    )
    src = src.replace(
        '<div class="rows" id="cases"></div>',
        '<div class="rows" id="cases">\n      ' + cases_html(data) + "\n    </div>",
    )
    src = src.replace(
        '<nav class="foot-apps" id="foot-apps" aria-label="Open an app"></nav>',
        '<nav class="foot-apps" id="foot-apps" aria-label="Open an app">\n        '
        + foot_apps_html(data)
        + "\n      </nav>",
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
    shots = docs / "shots"
    shots.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "shots", shots, dirs_exist_ok=True)
    (docs / ".nojekyll").touch()
    print("built %d apps -> %s" % (len(data), docs))


if __name__ == "__main__":
    main()
