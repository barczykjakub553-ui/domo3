/* Domokoncept — renders a single product page from products.json (?p=<slug>).
   Replaces ~800 static p-*.html files with one template + one JSON. */
(async () => {
  const root = document.getElementById('product-root');
  if (!root) return;
  const esc = s => (s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const notFound = () => {
    root.innerHTML = '<section class="page-hero"><div class="container">' +
      '<nav class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <a href="sklep.html">Sklep</a></nav>' +
      '<h1 class="page-hero__title">Nie znaleziono produktu</h1>' +
      '<p class="page-hero__sub"><a href="sklep.html">← Wróć do sklepu</a></p></div></section>';
  };

  const slug = new URLSearchParams(location.search).get('p');
  let index;
  try { index = await (await fetch('products.json')).json(); }
  catch (e) { notFound(); return; }
  const p = slug && index[slug];
  if (!p) { notFound(); return; }

  document.title = p.name + ' — Domokoncept';
  const md = document.querySelector('meta[name="description"]');
  if (md) md.content = p.name + ' — Domokoncept, salon meblowy Szczecin. Oferta na zapytanie.';

  const imgs = (p.imgs && p.imgs.length) ? p.imgs : [p.img];
  const thumbs = imgs.length > 1
    ? '<div class="gallery__thumbs">' + imgs.map((u, i) =>
        `<button class="gal__thumb${i === 0 ? ' is-active' : ''}" data-full="${esc(u)}" aria-label="Zdjęcie ${i + 1}"><img loading="lazy" src="${esc(u)}" alt="" /></button>`
      ).join('') + '</div>'
    : '';
  const desc = p.desc || [];
  const lead = desc[0] ? `<p class="product-lead">${esc(desc[0])}</p>` : '';
  const full = desc.length > 1
    ? '<section class="section section--flush product-desc"><div class="container"><h2>Opis produktu</h2>' +
      desc.slice(1).map(d => `<p>${esc(d)}</p>`).join('') + '</div></section>'
    : '';

  const card = q => `      <a class="product product--link" href="product.html?p=${q.slug}" data-cursor-hover data-name="${esc(q.name)}">
        <div class="product__media"><img loading="lazy" src="${esc(q.img)}" alt="${esc(q.name)}" />${q.outlet ? '<span class="product__tag">Outlet</span>' : ''}</div>
        <div class="product__info"><h3>${esc(q.name)}</h3><strong>Oferta na zapytanie</strong></div>
      </a>`;
  const rel = (p.rel || []).map(s => Object.assign({ slug: s }, index[s])).filter(q => q.name);
  const relHtml = rel.length
    ? '<section class="section section--flush"><div class="container"><header class="section__head"><p class="eyebrow">Zobacz też</p><h2 class="section__title">Podobne produkty</h2></header><div class="product-grid">' +
      rel.map(card).join('') + '</div></div></section>'
    : '';

  root.innerHTML = `
    <section class="page-hero page-hero--tight">
      <div class="container"><nav class="breadcrumb"><a href="sklep.html">Sklep</a> <span>/</span> <a href="k-${p.catSlug}.html">${esc(p.catTitle)}</a> <span>/</span> ${esc(p.name)}</nav></div>
    </section>
    <section class="section section--flush">
      <div class="container product-single">
        <div class="gallery" data-gallery>
          <div class="gallery__main"><img id="gal-main" src="${esc(imgs[0])}" alt="${esc(p.name)}" /></div>
          ${thumbs}
        </div>
        <div class="product-summary">
          <h1 class="product-single__title">${esc(p.name)}</h1>
          <div class="product-single__price">Oferta na zapytanie</div>
          ${lead}
          <div class="product-single__cta">
            <a href="kontakt.html" class="btn" data-cursor-hover>Zapytaj o produkt</a>
            <a href="tel:+48511891500" class="btn btn--ghost" data-cursor-hover>Zadzwoń · 511 891 500</a>
          </div>
          <ul class="product-single__meta">
            <li><span>Kategoria</span><span>${esc(p.catsMeta)}</span></li>
            <li><span>Raty</span><span>0% z Comfino</span></li>
            <li><span>Salon</span><span>Szczecin · 5 min od centrum</span></li>
          </ul>
        </div>
      </div>
    </section>
    ${full}
    ${relHtml}`;

  // gallery thumb switching (shop.js ran before this content existed)
  const gal = root.querySelector('[data-gallery]');
  const main = gal && gal.querySelector('#gal-main');
  if (gal && main) {
    gal.querySelectorAll('.gal__thumb').forEach(t => t.addEventListener('click', () => {
      main.src = t.dataset.full;
      gal.querySelectorAll('.gal__thumb').forEach(x => x.classList.remove('is-active'));
      t.classList.add('is-active');
    }));
  }
})();
