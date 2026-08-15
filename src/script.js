(function () {
  document.documentElement.classList.add("js");
  const apps = Array.isArray(window.APPS) ? window.APPS : [];
  const cases = document.getElementById("cases");
  const index = document.getElementById("index");
  const featured = document.getElementById("featured");
  const nav = document.getElementById("nav");
  const count = document.getElementById("shipped-count");

  const esc = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function cardHTML(app, i) {
    const n = pad(i + 1);
    const lazy = i < 2 ? "eager" : "lazy";
    const fetch = i === 0 ? "high" : "low";
    const fetchAttr = i === 0 ? ' fetchpriority="high"' : "";
    const paid = app.originalPaid ? "Replaces " + app.originalPaid : "";
    return `<article class="card" id="${esc(app.slug)}">
  <a class="still-link" href="${esc(app.pages)}">
    <div class="still-well">
      <img class="desk" src="${esc(app.desktop)}" alt="${esc(app.desktopAlt || app.name + " on desktop")}" width="1600" height="1000" loading="${lazy}" fetchpriority="${fetch}" decoding="async">
      <img class="phone" src="${esc(app.phone)}" alt="${esc(app.phoneAlt || app.name + " on a phone")}" width="390" height="844" loading="${lazy}" decoding="async">
    </div>
  </a>
  <div class="card-body">
    <div class="card-top">
      <p class="kicker">${esc(paid)}</p>
      <span class="n">${n}</span>
    </div>
    <h2>${esc(app.name)}</h2>
    <p class="job">${esc(app.job)}</p>
    <div class="actions">
      <a class="btn open" href="${esc(app.pages)}">Open <span class="arr" aria-hidden="true">→</span></a>
      <a class="btn src" href="${esc(app.repo)}" rel="noopener noreferrer">Source</a>
    </div>
  </div>
</article>`;
  }

  function featuredHTML(app) {
    if (!app) return "";
    return `<a class="frame-shot still-link" href="${esc(app.pages)}">
    <div class="still-well">
      <img class="desk" src="${esc(app.desktop)}" alt="${esc(app.desktopAlt || app.name + " on desktop")}" width="1600" height="1000" loading="eager" fetchpriority="high" decoding="async">
      <img class="phone" src="${esc(app.phone)}" alt="" width="390" height="844" loading="eager" decoding="async">
    </div>
  </a>
  <p class="frame-cap">
    <span class="kicker">Latest</span>
    <span class="frame-name">${esc(app.name)}</span>
    <span class="frame-go">Open →</span>
  </p>`;
  }

  function render() {
    if (count) count.textContent = pad(apps.length);

    if (index && !index.querySelector("a")) {
      index.innerHTML = apps
        .map(
          (app, i) =>
            `<a href="#${esc(app.slug)}" data-slug="${esc(app.slug)}"><span class="n">${pad(i + 1)}</span> ${esc(app.name)}</a>`
        )
        .join("");
    }

    if (featured && !featured.querySelector(".frame-shot") && apps.length) {
      featured.innerHTML = featuredHTML(apps[apps.length - 1]);
    }

    if (cases && !cases.querySelector(".card")) {
      cases.innerHTML = apps.map(cardHTML).join("");
    }
  }

  function observe() {
    const nodes = document.querySelectorAll(".card");
    const links = [...document.querySelectorAll("#index a")];
    if (!nodes.length) return;

    const setOn = (slug) => {
      links.forEach((a) => a.classList.toggle("is-on", a.dataset.slug === slug));
    };

    if (nodes[0]) setOn(nodes[0].id);

    if (!("IntersectionObserver" in window)) return;

    const spy = new IntersectionObserver(
      (entries) => {
        const vis = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (vis) setOn(vis.target.id);
      },
      { threshold: [0.25, 0.45, 0.7], rootMargin: "-20% 0px -40% 0px" }
    );
    nodes.forEach((el) => spy.observe(el));
  }

  function onScroll() {
    if (!nav) return;
    nav.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  if (/[?&]proof\b/.test(location.search)) {
    document.documentElement.classList.add("proof");
  }

  render();
  if (location.hash) {
    const el = document.getElementById(location.hash.slice(1));
    if (el) el.scrollIntoView();
  }
  const shot = new URLSearchParams(location.search).get("shot");
  if (shot) {
    const el = document.getElementById(shot);
    if (el) el.scrollIntoView({ block: "center" });
  }
  observe();
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
