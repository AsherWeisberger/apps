(function () {
  document.documentElement.classList.add("js");
  const apps = Array.isArray(window.APPS) ? window.APPS : [];
  const cases = document.getElementById("cases");
  const index = document.getElementById("index");
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

  function kinetic(name) {
    return esc(name)
      .split(/\s+/)
      .map((w) => `<span class="clip"><span class="word">${w}</span></span>`)
      .join(" ");
  }

  function shipped(iso) {
    if (!iso) return "";
    const d = new Date(iso + "T00:00:00");
    if (Number.isNaN(d.getTime())) return "";
    const mon = d.toLocaleString("en-US", { month: "short" });
    return `Shipped ${d.getDate()} ${mon} ${d.getFullYear()}`;
  }

  function render() {
    if (!cases || !index) return;
    if (count) count.textContent = pad(apps.length);

    if (cases.querySelectorAll(".case").length) return;

    index.innerHTML = apps
      .map(
        (app, i) =>
          `<a href="#${esc(app.slug)}" data-slug="${esc(app.slug)}"><span class="n">${pad(i + 1)}</span>${esc(app.name)}</a>`
      )
      .join("");

    cases.innerHTML = apps
      .map((app, i) => {
        const n = pad(i + 1);
        const flip = i % 2 === 1 ? " flip" : "";
        const shown = i === 0 ? " in" : "";
        const lazy = i === 0 ? "eager" : "lazy";
        const fetch = i === 0 ? "high" : "low";
        const when = shipped(app.shipped);
        return `
<section class="case${flip}${shown}" id="${esc(app.slug)}" data-n="${n}">
  <header class="case-head">
    <p class="idx">${n}</p>
    <div class="titles">
      <h2>${kinetic(app.name)}</h2>
      <p class="job">${esc(app.job)}</p>
      ${when ? `<p class="meta">${esc(when)}</p>` : ""}
    </div>
    <div class="actions">
      <a class="btn open" href="${esc(app.pages)}">Open live <span class="arr" aria-hidden="true">→</span></a>
      <a class="btn src" href="${esc(app.repo)}" rel="noopener noreferrer">Source</a>
    </div>
  </header>
  <div class="stills">
    <figure class="desk">
      <img src="${esc(app.desktop)}" alt="${esc(app.desktopAlt || app.name + " on desktop")}" width="1600" height="1000" loading="${lazy}" fetchpriority="${fetch}" decoding="async">
      <figcaption class="cap">Desktop</figcaption>
    </figure>
    <figure class="phone">
      <img src="${esc(app.phone)}" alt="${esc(app.phoneAlt || app.name + " on a phone")}" width="390" height="844" loading="${lazy}" decoding="async">
      <figcaption class="cap">390</figcaption>
    </figure>
  </div>
</section>`;
      })
      .join("");
  }

  function observe() {
    const nodes = document.querySelectorAll(".case");
    const links = [...document.querySelectorAll("#index a")];
    if (!nodes.length) return;

    const setOn = (slug) => {
      links.forEach((a) => a.classList.toggle("is-on", a.dataset.slug === slug));
    };

    const reveal = (el) => el.classList.add("in");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (nodes[0]) {
      reveal(nodes[0]);
      setOn(nodes[0].id);
    }
    nodes.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) reveal(el);
    });

    if (reduce || !("IntersectionObserver" in window)) {
      nodes.forEach(reveal);
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            reveal(e.target);
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0 }
    );
    nodes.forEach((el) => io.observe(el));

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
