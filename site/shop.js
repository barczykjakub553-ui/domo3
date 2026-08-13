/* Domokoncept — product gallery + listing price filter/sort. No dependencies. */
(() => {
  /* ---------- product-page gallery ---------- */
  const gal = document.querySelector('[data-gallery]');
  if (gal) {
    const main = gal.querySelector('#gal-main');
    gal.querySelectorAll('.gal__thumb').forEach(t => {
      t.addEventListener('click', () => {
        if (main) main.src = t.dataset.full;
        gal.querySelectorAll('.gal__thumb').forEach(x => x.classList.remove('is-active'));
        t.classList.add('is-active');
      });
    });
  }

  /* ---------- listing filters + sort ---------- */
  const grid = document.querySelector('[data-grid]');
  const bar = document.querySelector('[data-filters]');
  if (!grid || !bar) return;
  const items = [...grid.querySelectorAll('.product')];   // original DOM order
  const sort = bar.querySelector('#f-sort');
  if (!sort) return;

  sort.addEventListener('change', () => {
    let vis = items.slice();
    if (sort.value === 'name') {
      vis.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name, 'pl'));
    }
    // 'default' keeps original DOM order
    vis.forEach(el => grid.appendChild(el));
  });
})();
