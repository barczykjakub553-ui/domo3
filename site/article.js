/* Domokoncept — renders a single blog article from articles.json (?a=<slug>).
   Replaces the static b-*.html files with one template + one JSON. */
(async () => {
  const root = document.getElementById('article-root');
  if (!root) return;
  const esc = s => (s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const notFound = () => {
    root.innerHTML = '<section class="page-hero"><div class="container">' +
      '<nav class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <a href="blog.html">Baza wiedzy</a></nav>' +
      '<h1 class="page-hero__title">Nie znaleziono artykułu</h1>' +
      '<p class="page-hero__sub"><a href="blog.html">← Wróć do bazy wiedzy</a></p></div></section>';
  };

  const slug = new URLSearchParams(location.search).get('a');
  let index;
  try { index = await (await fetch('articles.json')).json(); }
  catch (e) { notFound(); return; }
  const a = slug && index[slug];
  if (!a) { notFound(); return; }

  document.title = a.title + ' — Domokoncept';
  const md = document.querySelector('meta[name="description"]');
  if (md && a.excerpt) md.content = a.excerpt;

  const paras = (a.paras || []).map(p => `<p>${esc(p)}</p>`).join('');
  const heroImg = a.img ? `<div class="article__hero" style="background-image:url('${esc(a.img)}')"></div>` : '';

  root.innerHTML = `
    <section class="page-hero page-hero--tight">
      <div class="container"><nav class="breadcrumb"><a href="index.html">Home</a> <span>/</span> <a href="blog.html">Baza wiedzy</a> <span>/</span> ${esc(a.title)}</nav></div>
    </section>
    <article class="section section--flush"><div class="container article">
      <h1 class="article__title">${esc(a.title)}</h1>
      ${heroImg}
      <div class="article__body prose">${paras}</div>
      <div class="hero__cta" style="margin-top:36px"><a href="blog.html" class="btn btn--ghost" data-cursor-hover>← Wróć do bazy wiedzy</a><a href="sklep.html" class="btn" data-cursor-hover>Przeglądaj sklep</a></div>
    </div></article>`;
})();
