(function(){
  var proof = /\bproof\b/.test(location.search);
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (proof) document.documentElement.classList.add("proof");

  var apps = Array.isArray(window.APPS) ? window.APPS.slice().reverse() : [];
  var shop = document.getElementById("shop");
  var chips = document.getElementById("chips");
  var island = document.getElementById("island");
  var orbHost = document.getElementById("island-orb");

  function esc(s){
    return String(s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }
  function num(i){ return String(i + 1).padStart(2, "0"); }
  function stillSrc(app){ return esc(app.still || ("./shots/" + app.slug + "/card.webp")); }
  function phoneSrc(app){ return esc(app.phoneWebp || ("./shots/" + app.slug + "/phone.webp")); }

  function card(app, i){
    var featured = i === 0 ? " featured" : "";
    var lazy = i < 2 ? "eager" : "lazy";
    var fetch = i === 0 ? ' fetchpriority="high"' : "";
    var kicker = esc(app.kicker || (app.originalPaid ? "Original alternative" : "Browser utility"));
    return '<article class="card' + featured + ' reveal" id="' + esc(app.slug) + '">' +
      '<a class="still" href="' + esc(app.pages) + '" aria-label="Open ' + esc(app.name) + '">' +
        '<picture>' +
          '<source media="(max-width:700px)" srcset="' + phoneSrc(app) + '">' +
          '<img src="' + stillSrc(app) + '" alt="' + esc(app.desktopAlt || app.name) + '" width="1440" height="900" loading="' + lazy + '"' + fetch + ' decoding="async">' +
        '</picture>' +
        (i === 0 ? '<img class="device" src="' + phoneSrc(app) + '" alt="" width="390" height="844" decoding="async">' : "") +
        '<span class="open-chip">Open</span>' +
      '</a>' +
      '<div class="meta">' +
        '<div class="card-top"><span class="number">' + num(i) + '</span><span>' + kicker + '</span></div>' +
        '<h2 data-name="' + esc(app.name) + '">' + esc(app.name) + '</h2>' +
        '<p class="card-copy">' + esc(app.job) + '</p>' +
        '<div class="links">' +
          '<a class="btn primary" href="' + esc(app.pages) + '">Open<span class="fill" aria-hidden="true"></span></a>' +
          '<a class="btn" href="' + esc(app.repo) + '" rel="noopener noreferrer">Source<span class="fill" aria-hidden="true"></span></a>' +
        '</div>' +
      '</div>' +
    '</article>';
  }

  function chip(app, i){
    return '<a href="#' + esc(app.slug) + '"><em>' + num(i) + '</em>' + esc(app.name) + '</a>';
  }

  if (shop && !shop.querySelector(".card")) shop.innerHTML = apps.map(card).join("");
  if (chips && !chips.querySelector("a")) chips.innerHTML = apps.map(chip).join("");

  var orb = null;
  if (island && orbHost && window.KitOrb && !proof && !reduced) {
    document.body.classList.add("boot");
    orb = window.KitOrb.createOrb(orbHost, { state: "working", theme: "dark" });
    requestAnimationFrame(function(){ island.classList.add("is-open"); });
    setTimeout(function(){
      island.classList.add("is-gone");
      document.body.classList.remove("boot");
      document.body.classList.add("ready");
      setTimeout(function(){
        if (orb) { orb.destroy(); orb = null; }
        island.setAttribute("hidden", "");
      }, 480);
    }, 1100);
  } else {
    document.body.classList.add("ready");
    if (island) island.setAttribute("hidden", "");
  }

  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting) { e.target.classList.add("seen"); obs.unobserve(e.target); }
    });
  }, { threshold: 0.06, rootMargin: "40px 0px" });
  document.querySelectorAll(".reveal").forEach(function(el, i){
    if (i < 2 || proof) { el.classList.add("seen"); return; }
    obs.observe(el);
  });

  if (!reduced && !proof && window.matchMedia("(hover:hover) and (pointer:fine)").matches) {
    document.querySelectorAll(".card h2").forEach(function(el){
      el.addEventListener("mouseenter", function(){
        var orig = el.getAttribute("data-name") || el.textContent;
        var glyphs = orig.replace(/\s/g, "");
        if (!glyphs) return;
        var n = 0;
        var t = setInterval(function(){
          el.textContent = orig.split("").map(function(ch){
            if (ch === " " || n > 4) return ch;
            return glyphs.charAt(Math.floor(Math.random() * glyphs.length));
          }).join("");
          n++;
          if (n > 5) { clearInterval(t); el.textContent = orig; }
        }, 28);
      });
    });
  }
})();
