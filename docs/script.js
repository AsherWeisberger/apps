(function () {
  const apps = Array.isArray(window.APPS) ? window.APPS.slice() : [];
  const newestFirst = apps.slice().reverse();
  const grid = document.getElementById("grid");
  const island = document.getElementById("island");

  const esc = (s) =>
    String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  function stillSrc(app) {
    return app.still || "./shots/" + app.slug + "/pack.png";
  }

  function cardHTML(app, i) {
    const lazy = "eager";
    const fetchAttr = i === 0 ? ' fetchpriority="high"' : "";
    const paid = app.originalPaid ? "Replaces " + app.originalPaid : "";
    const src = esc(stillSrc(app));
    const alt = esc(app.desktopAlt || app.name);
    return `<article class="card" id="${esc(app.slug)}">
  <a class="still" href="${esc(app.pages)}">
    <img src="${src}" alt="${alt}" width="1200" height="1200" loading="${lazy}"${fetchAttr} decoding="async">
  </a>
  <h2>${esc(app.name)}</h2>
  ${paid ? `<p class="meta">${esc(paid)}</p>` : `<p class="meta">${esc(app.job || "")}</p>`}
  <a class="open" href="${esc(app.pages)}">Open</a>
  <a class="src" href="${esc(app.repo)}" rel="noopener noreferrer">Source</a>
</article>`;
  }

  if (grid && !grid.querySelector(".card") && newestFirst.length) {
    grid.innerHTML = newestFirst.map(cardHTML).join("");
  }

  const latest = apps.length ? apps[apps.length - 1] : null;
  if (island && latest) {
    island.href = latest.pages;
    island.textContent = "Open " + latest.name;
    island.removeAttribute("hidden");
  }
})();
