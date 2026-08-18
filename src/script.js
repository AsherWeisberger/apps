(function(){
  if(/\bproof\b/.test(location.search)) document.documentElement.classList.add("proof");
  const apps=Array.isArray(window.APPS)?window.APPS.slice().reverse():[];
  const grid=document.getElementById("grid");
  const esc=s=>String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  const card=(app,i)=>`<article class="card reveal" id="${esc(app.slug)}">
    <div class="card-top"><span class="number">0${i+1}</span><span>${esc(app.originalPaid?"Original alternative":"Browser utility")}</span></div>
    <a class="still" href="${esc(app.pages)}" aria-label="Open ${esc(app.name)}"><img src="${esc(app.still||"./shots/"+app.slug+"/pack.png")}" alt="${esc(app.desktopAlt||app.name)}" width="1200" height="750" loading="${i<2?"eager":"lazy"}" decoding="async"${i===0?' fetchpriority="high"':''}></a>
    <div class="card-info"><div><h2>${esc(app.name)}</h2><p class="card-copy">${esc(app.job)}</p></div><div class="links"><a class="button primary" href="${esc(app.pages)}">Open app ↗</a><a class="button" href="${esc(app.repo)}" rel="noopener noreferrer">Source</a></div></div>
  </article>`;
  if(grid && !grid.querySelector(".card")) grid.innerHTML=apps.map(card).join("");
  const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("seen");obs.unobserve(e.target)}}),{threshold:.06,rootMargin:"40px 0px"});
  document.querySelectorAll(".reveal").forEach((el,i)=>{
    if(i<2 || document.documentElement.classList.contains("proof")){el.classList.add("seen");return;}
    obs.observe(el);
  });
})();
