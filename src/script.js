/* Filters existing static cards; all tools remain available without JavaScript. */
(() => {
  const input = document.getElementById('search-tools');
  const cards = [...document.querySelectorAll('.tool-card')];
  const categories = [...document.querySelectorAll('.category')];
  const clear = document.getElementById('clear-search');
  let category = 'All tools';
  function update() {
    const query = input.value.trim().toLowerCase();
    let count = 0;
    for (const card of cards) {
      const visible = (category === 'All tools' || card.dataset.category === category) && card.dataset.search.includes(query);
      card.hidden = !visible;
      if (visible) count++;
    }
    for (const button of categories) {
      const selected = button.dataset.category === category;
      button.classList.toggle('selected', selected);
      button.setAttribute('aria-pressed', String(selected));
    }
    document.getElementById('category-title').textContent = category;
    document.getElementById('breadcrumb-category').textContent = category;
    document.getElementById('result-count').textContent = count;
    document.getElementById('result-summary').textContent = query ? `${count} ${count === 1 ? 'tool' : 'tools'} matching “${input.value.trim()}”` : 'Pick a tool. Everything opens in your browser.';
    document.getElementById('empty-state').hidden = count !== 0;
    clear.hidden = input.value.length === 0;
  }
  function reset() { category = 'All tools'; input.value = ''; update(); }
  categories.forEach(button => button.addEventListener('click', () => { category = button.dataset.category; update(); }));
  input.addEventListener('input', update);
  clear.addEventListener('click', () => { input.value = ''; update(); input.focus(); });
  document.getElementById('reset-home').addEventListener('click', reset);
  document.getElementById('show-all').addEventListener('click', () => { reset(); input.focus(); });
  // Preserve direct links to individual tools after filtering.
  window.addEventListener('hashchange', () => {
    const target = cards.find(card => `#${card.id}` === location.hash);
    if (target && target.hidden) { reset(); target.scrollIntoView(); }
  });
})();
