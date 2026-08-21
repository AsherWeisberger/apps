# Asher · apps

A dark editorial shop of free, original in-tab apps. No account. No watermark. Files never leave the browser.

Live: [asherweisberger.github.io/apps](https://asherweisberger.github.io/apps/)

Made by [Asher Weisberger](https://x.com/AsherWeisberger) ([@AsherWeisberger](https://x.com/AsherWeisberger))

The page is a tight dark storefront: Motion palette (`#0D0F14` ink, `#D9CCAC` sand), a short kinetic line, then the apps as photo-dominant cards. Newest first. Each card is a still of the live UI, one plain sentence, Open, and Source. JSON order is oldest → newest; the shop shows newest first.

Pitches are one sentence a 10-year-old gets.

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

Static HTML, CSS, JS. Motion palette on a dark field, self-hosted Geist Sans (SIL OFL). No framework, no bundler, no account.

MIT. Copyright 2026 Asher Weisberger ([@AsherWeisberger](https://x.com/AsherWeisberger)). Original work — not affiliated with the paid apps these replace.

Geist Sans © 2023 Vercel, SIL Open Font License 1.1. See `src/fonts/LICENSE`.
