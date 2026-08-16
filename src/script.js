(function () {
  document.documentElement.classList.add("js");
  const apps = Array.isArray(window.APPS) ? window.APPS : [];
  const cases = document.getElementById("cases");
  const featured = document.getElementById("featured");
  const footApps = document.getElementById("foot-apps");
  const nav = document.getElementById("nav");

  const esc = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  function stillSrc(app) {
    return app.still || app.desktop;
  }

  function rowHTML(app, i) {
    const lazy = i < 2 ? "eager" : "lazy";
    const fetchAttr = i === 0 ? ' fetchpriority="high"' : "";
    const flip = i % 2 === 1 ? " is-flip" : "";
    const paid = app.originalPaid ? "Replaces " + app.originalPaid : "";
    const src = esc(stillSrc(app));
    const alt = esc(app.desktopAlt || app.name + " editor");
    return `<article class="row${flip}" id="${esc(app.slug)}" style="--i:${i}">
  <a class="row-still" href="${esc(app.pages)}">
    <figure>
      <img src="${src}" alt="${alt}" width="1600" height="1000" loading="${lazy}"${fetchAttr} decoding="async">
    </figure>
  </a>
  <div class="row-copy">
    ${paid ? `<p class="kicker">${esc(paid)}</p>` : ""}
    <h2>${esc(app.name)}</h2>
    <p class="job">${esc(app.job)}</p>
    <div class="actions">
      <a class="btn open" href="${esc(app.pages)}">Open <span class="arr" aria-hidden="true">→</span></a>
      <a class="src" href="${esc(app.repo)}" rel="noopener noreferrer">Source</a>
    </div>
  </div>
</article>`;
  }

  function featuredHTML(app) {
    if (!app) return "";
    const src = esc(stillSrc(app));
    const alt = esc(app.desktopAlt || app.name + " editor");
    return `<a class="hero-frame" href="${esc(app.pages)}">
    <figure>
      <img src="${src}" alt="${alt}" width="1600" height="1000" loading="eager" fetchpriority="high" decoding="async">
    </figure>
    <p class="hero-cap">
      <span class="kicker">Latest</span>
      <span class="hero-name">${esc(app.name)}</span>
    </p>
  </a>`;
  }

  function render() {
    if (featured && !featured.querySelector(".hero-frame") && apps.length) {
      featured.innerHTML = featuredHTML(apps[apps.length - 1]);
    }
    if (cases && !cases.querySelector(".row")) {
      cases.innerHTML = apps.map(rowHTML).join("");
    }
    if (footApps && !footApps.querySelector("a")) {
      footApps.innerHTML = apps
        .map((app) => `<a href="${esc(app.pages)}">${esc(app.name)}</a>`)
        .join("");
    }
  }

  function settle() {
    const rows = document.querySelectorAll(".row");
    if (!rows.length) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !("IntersectionObserver" in window)) return;

    rows.forEach((el) => el.classList.add("will-settle"));

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.16, rootMargin: "0px 0px -6% 0px" }
    );
    rows.forEach((el) => io.observe(el));

    window.setTimeout(() => {
      rows.forEach((el) => el.classList.add("is-in"));
    }, 1400);
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
  settle();
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
