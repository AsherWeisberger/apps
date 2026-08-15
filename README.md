# Asher · apps

A studio index of free, original in-tab apps. No account. No watermark. Files never leave the browser.

Live: [asherweisberger.github.io/apps](https://asherweisberger.github.io/apps/)

Made by [Asher Weisberger](https://x.com/AsherWeisberger) ([@AsherWeisberger](https://x.com/AsherWeisberger))

This is a catalog, not a dashboard. Each shipped app is a card: desktop still, 390 still, one-line job, Open, and Source.

## Add the next daily app

Nightly builds should **append**, not rewrite the page by hand.

1. Drop stills into `shots/<slug>/desktop.png` and `shots/<slug>/phone.png`. Copy them into this repo — do not hotlink.
2. Append one object to `apps.json` at the repo root:

```json
{
  "slug": "newapp",
  "name": "NewApp",
  "job": "One line. What it does. Files stay in the tab.",
  "pages": "https://asherweisberger.github.io/newapp/",
  "repo": "https://github.com/AsherWeisberger/newapp",
  "originalPaid": "The paid job it replaces",
  "shipped": "2026-08-15",
  "desktop": "./shots/newapp/desktop.png",
  "phone": "./shots/newapp/phone.png",
  "desktopAlt": "NewApp on desktop.",
  "phoneAlt": "NewApp on a phone."
}
```

3. Run `./build.sh`. It writes `apps.js`, copies the site into `docs/`, and writes a slim machine list at `docs/apps.json`:

```
[{slug, name, job, pages, repo, originalPaid, shipped}]
```

4. Commit `apps.json`, `apps.js`, `shots/<slug>/`, and everything under `docs/`. Push `main`. Pages serves `/docs`.

The page reads `apps.js` (`window.APPS`) and renders the case studies. Order in the JSON is the order on the page.

Do not add GitHub Actions workflows. This repo uses legacy Pages from `main` `/docs`.

## Local

```
./build.sh
python3 -m http.server 8080 --directory docs
```

Then open http://127.0.0.1:8080/

## Stack

Static HTML, CSS, JS. Cream catalog. Sora 400/600 + Fraunces italic. No framework, no bundler, no account.

MIT. Copyright 2026 Asher Weisberger ([@AsherWeisberger](https://x.com/AsherWeisberger)). Original work — not affiliated with the paid apps these replace.
