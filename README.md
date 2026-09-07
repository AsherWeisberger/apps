# Asher · apps

A responsive library of free browser tools, with task search, category navigation, and compact app previews.

Live: [asherweisberger.github.io/apps](https://asherweisberger.github.io/apps/)

Made by [Asher Weisberger](https://x.com/AsherWeisberger).

## Add the next daily app

Nightly builds should **append**, not rewrite the page by hand.

1. Drop stills into `shots/<slug>/desktop.png` and `shots/<slug>/phone.png`. Copy them into this repo — do not hotlink.
2. Append one object to `apps.json` at the repo root:

```json
{
  "slug": "newapp",
  "name": "NewApp",
  "job": "One line. What it does.",
  "kicker": "Short verb",
  "category": "PDF & documents",
  "description": "A clear description of the task.",
  "pages": "https://asherweisberger.github.io/newapp/",
  "repo": "https://github.com/AsherWeisberger/newapp",
  "originalPaid": "The paid job it replaces",
  "shipped": "2026-08-21",
  "desktop": "./shots/newapp/desktop.png",
  "phone": "./shots/newapp/phone.png",
  "desktopAlt": "NewApp on desktop.",
  "phoneAlt": "NewApp on a phone."
}
```

Categories: `PDF & documents`, `Images`, `Design`, `Video & audio`, and `Text & code`. Apps without a category appear under `Other tools`. The displayed total updates automatically.

`./build.sh` writes `card.webp` / `phone.webp` gallery stills and a square packshot at `shots/<slug>/pack.png`. Set `"still"` to skip pack generation and use your own frame. `"packAlign": "right"` (or `"left"`) shifts the square crop.

3. Run `./build.sh`. It writes `apps.js`, copies the site into `docs/`, and writes a slim machine list at `docs/apps.json`.

4. Commit `apps.json`, `apps.js`, `shots/<slug>/`, and everything under `docs/`. Push `main`. Pages serves `/docs`.

Do not add GitHub Actions workflows. This repo uses legacy Pages from `main` `/docs`.

## Local

```
./build.sh
python3 -m http.server 8080 --directory docs
```

Then open http://127.0.0.1:8080/

## Stack

Static HTML, CSS, and JavaScript with self-hosted Geist Sans (SIL OFL). White and indigo UI, responsive category navigation, accessible search and empty states. All app links remain available without JavaScript. No framework or bundler.

MIT. Copyright 2026 Asher Weisberger ([@AsherWeisberger](https://x.com/AsherWeisberger)). Original work — not affiliated with the paid apps these replace.

Geist Sans © 2023 Vercel, SIL Open Font License 1.1. See `src/fonts/LICENSE`.
