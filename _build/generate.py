#!/usr/bin/env python3
"""Full site generator: product pages (galleries), category/arrangement listings
with price filter + sorting, sklep/aranzacje landings, content pages.
Reuses the template components; deployed output is pure static HTML."""
import json, html, os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, "..", "site"))
products = json.load(open(os.path.join(HERE, "products_full.json"), encoding="utf-8"))

def esc(s): return html.escape(s or "", quote=True)
def slug_of(url): return url.rstrip("/").split("/")[-1]
for p in products:
    p["slug"] = slug_of(p["url"])

CATS = OrderedDict([
    ("sofy", ("Sofy i narożniki", "Kanapy, narożniki, sofy klasyczne i biurowe",
              {"sofy","sofy-nowoczesne","sofy-klasyczne","sofy-biurowe","sofa-narozna","sofa-rozkladana-z-funkcja-spania","narozniki"})),
    ("sofy-modulowe", ("Sofy modułowe", "Elastyczne systemy, które składasz pod swój salon",
              {"sofa-modulowa","system-modulowy"})),
    ("stoly", ("Stoły", "Stoły stałe i rozkładane, w tym okrągłe",
              {"stoly","stoly-rozkladane","stoly-okragle","stol-okragly-rozkladany"})),
    ("stoliki", ("Stoliki kawowe", "Stoliki i ławy do salonu", {"stoliki-i-lawy"})),
    ("krzesla", ("Krzesła", "Krzesła do jadalni i salonu", {"krzesla"})),
    ("fotele", ("Fotele", "Fotele wypoczynkowe i obrotowe", {"fotele"})),
    ("hokery", ("Krzesła barowe i hokery", "Hokery i krzesła barowe", {"krzesla-barowe-i-hokery","hokery"})),
    ("komody", ("Komody i komody RTV", "Komody, szafki RTV i przechowywanie", {"komody","komody-rtv"})),
    ("oswietlenie", ("Oświetlenie", "Lampy wiszące, stojące i punktowe", {"oswietlenie","wiszace"})),
    ("dywany", ("Dywany", "Dywany do salonu, sypialni i jadalni", {"dywany"})),
    ("dodatki", ("Dodatki", "Poduszki, akcesoria i dekoracje", {"dodatki","akcesoria","poduszki"})),
    ("meble", ("Meble i pozostałe", "Łóżka, regały, biurka, pufy, wieszaki i meble luksusowe",
              {"lozka","regaly-i-polki","polki-i-konsole","biurka","szafki","luksusowe-meble","pufy","wieszaki","lawki-meble","hustawki"})),
    ("outlet", ("Outlet", "Ekspozycje i końcówki serii w niższych cenach", {"outlet"})),
])
ROOMS = OrderedDict([
    ("sypialnia", ("Sypialnia", "Łóżka, komody, oświetlenie i dodatki do sypialni", "https://domokoncept.pl/wp-content/uploads/2022/05/sypialnia.jpg")),
    ("salon", ("Salon", "Sofy, stoliki, dywany i lampy do salonu", "https://domokoncept.pl/wp-content/uploads/2022/05/salon.jpg")),
    ("jadalnia", ("Jadalnia", "Stoły, krzesła i oświetlenie do jadalni", "https://domokoncept.pl/wp-content/uploads/2022/05/jadalnia-1.jpg")),
    ("przedpokoj", ("Przedpokój", "Wieszaki, ławki, lustra i drobne meble", "https://domokoncept.pl/wp-content/uploads/2022/05/przedpokoj-1.jpg")),
])
def in_cat(p, s): return bool(set(p["cats"]) & s)
cat_products = {c: [] for c in CATS}; matched = set()
for i, p in enumerate(products):
    for c, (_, _, s) in CATS.items():
        if c == "meble": continue
        if in_cat(p, s): cat_products[c].append(p); matched.add(i)
mset = CATS["meble"][2]
for i, p in enumerate(products):
    if in_cat(p, mset) or i not in matched: cat_products["meble"].append(p)
room_products = {r: [p for p in products if r in p.get("rooms", [])] for r in ROOMS}
# primary category per product (for breadcrumb + related)
def primary_cat(p):
    for c, (_, _, s) in CATS.items():
        if c != "meble" and in_cat(p, s): return c
    return "meble"

# ---------------- chrome ----------------
CAT_LINKS = "".join(f'<a href="k-{c}.html">{esc(t)}</a>' for c,(t,_,_) in CATS.items())
ROOM_LINKS = "".join(f'<a href="a-{r}.html">{esc(t)}</a>' for r,(t,_,_) in ROOMS.items())
TOPBAR = '''  <div class="topbar"><div class="container topbar__inner">
    <span>Salon meblowy w Szczecinie · niespełna 5 minut od centrum</span>
    <span class="topbar__hours">Pon–Pt 10:30–17:00 · Sob 10:00–14:00</span>
  </div></div>'''

def header(active=""):
    def cur(x): return " is-current" if x==active else ""
    return TOPBAR + f'''
  <header class="header header--solid" data-header>
    <div class="container header__inner">
      <a href="index.html" class="logo" data-cursor-hover>DOMOKONCEPT</a>
      <nav class="nav" data-nav>
        <span class="nav__item has-dropdown">
          <a href="sklep.html" class="nav__link{cur('sklep')}" data-cursor-hover>Sklep</a>
          <span class="dropdown">{CAT_LINKS}</span>
        </span>
        <span class="nav__item has-dropdown">
          <a href="aranzacje.html" class="nav__link{cur('aranzacje')}" data-cursor-hover>Aranżacje</a>
          <span class="dropdown">{ROOM_LINKS}</span>
        </span>
        <a href="marki.html" class="nav__link{cur('marki')}" data-cursor-hover>Marki</a>
        <a href="o-nas.html" class="nav__link{cur('o-nas')}" data-cursor-hover>O nas</a>
        <a href="kontakt.html" class="nav__link{cur('kontakt')}" data-cursor-hover>Kontakt</a>
      </nav>
      <div class="header__actions">
        <a href="tel:+48511891500" class="btn btn--small" data-cursor-hover>Zadzwoń · 511 891 500</a>
        <button class="burger" data-burger aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>'''

FOOTER = f'''  <footer class="footer">
    <div class="container footer__grid">
      <div class="footer__brand"><span class="logo">DOMOKONCEPT</span><p>…inna strona wnętrza. Salon meblowy w Szczecinie.</p></div>
      <div class="footer__col"><h4>Sklep</h4>
        <a href="k-sofy.html" data-cursor-hover>Sofy i narożniki</a>
        <a href="k-stoly.html" data-cursor-hover>Stoły</a>
        <a href="k-krzesla.html" data-cursor-hover>Krzesła</a>
        <a href="k-oswietlenie.html" data-cursor-hover>Oświetlenie</a>
        <a href="k-outlet.html" data-cursor-hover>Outlet</a>
        <a href="sklep.html" data-cursor-hover>Wszystkie kategorie</a></div>
      <div class="footer__col"><h4>Firma</h4>
        <a href="o-nas.html" data-cursor-hover>O nas</a>
        <a href="marki.html" data-cursor-hover>Marki</a>
        <a href="blog.html" data-cursor-hover>Baza wiedzy</a>
        <a href="comfino.html" data-cursor-hover>Raty Comfino</a>
        <a href="pomoc.html" data-cursor-hover>Pomoc</a>
        <a href="regulamin.html" data-cursor-hover>Regulamin</a>
        <a href="polityka-prywatnosci.html" data-cursor-hover>Polityka prywatności</a></div>
      <div class="footer__col"><h4>Kontakt</h4>
        <a href="tel:+48511891500" data-cursor-hover>+48 511 891 500</a>
        <a href="mailto:salon@domokoncept.pl" data-cursor-hover>salon@domokoncept.pl</a>
        <a href="kontakt.html" data-cursor-hover>Szczecin · 5 min od centrum</a>
        <a href="https://instagram.com/domokoncept" target="_blank" rel="noopener" data-cursor-hover>Instagram</a></div>
    </div>
    <div class="container footer__bar"><span>© 2026 Domokoncept — salon meblowy w Szczecinie.</span><span>Poczuj się jak u siebie w domu.</span></div>
  </footer>'''

def page(title, active, body, desc=""):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{esc(desc)}" />
  <title>{esc(title)} — Domokoncept</title>
  <link rel="icon" href="images/logo.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v=4" />
</head>
<body>
  <div class="cursor" data-cursor aria-hidden="true"><div class="cursor__dot"></div><div class="cursor__ring"></div></div>
  <div class="progress" data-progress aria-hidden="true"></div>
{header(active)}
  <main class="subpage">
{body}
  </main>
{FOOTER}
  <script src="main.js"></script>
  <script src="shop.js"></script>
</body>
</html>
'''

def product_card(p):
    price = "Oferta na zapytanie"
    tag = '<span class="product__tag">Outlet</span>' if "outlet" in p["cats"] else ""
    return f'''      <a class="product product--link" href="product.html?p={p['slug']}" data-cursor-hover data-name="{esc(p['name'])}">
        <div class="product__media"><img loading="lazy" src="{esc(p['img'])}" alt="{esc(p['name'])}" />{tag}</div>
        <div class="product__info"><h3>{esc(p['name'])}</h3><strong>{price}</strong></div>
      </a>'''

def filter_bar(prods, total):
    return f'''      <div class="filters" data-filters>
        <div class="filters__group">
          <label for="f-sort">Sortuj</label>
          <select id="f-sort">
            <option value="default">Domyślne</option>
            <option value="name">Nazwa: A–Z</option>
          </select>
        </div>
        <span class="filters__count"><strong id="f-count">{total}</strong> produktów</span>
      </div>'''

def page_hero(crumb, title, subtitle, count=None):
    cnt = f'<span class="page-hero__count">{count} produktów</span>' if count is not None else ''
    sub = f'<p class="page-hero__sub" data-reveal>{esc(subtitle)} {cnt}</p>' if subtitle or cnt else ''
    return f'''    <section class="page-hero">
      <div class="container">
        <nav class="breadcrumb" data-reveal><a href="index.html">Home</a> <span>/</span> {crumb}</nav>
        <h1 class="page-hero__title" data-reveal>{esc(title)}</h1>
        {sub}
      </div>
    </section>'''

def listing_page(fname, title, subtitle, prods, crumb, active, desc):
    cards = "\n".join(product_card(p) for p in prods) or '<p class="empty">Wkrótce nowe produkty w tej kategorii.</p>'
    body = page_hero(crumb, title, subtitle, len(prods)) + f'''
    <section class="section section--flush">
      <div class="container">
{filter_bar(prods, len(prods))}
        <div class="product-grid" data-grid>
{cards}
        </div>
      </div>
    </section>'''
    open(os.path.join(SITE, fname), "w", encoding="utf-8").write(page(title, active, body, desc))

# ---------------- product data (one JSON) + one dynamic template ----------------
# Instead of ~800 static p-*.html files, emit a single products.json and one
# product.html shell that renders any product client-side from ?p=<slug>.
def product_data(p):
    pc = primary_cat(p)
    cats_meta = " · ".join(CATS[c][0] for c in CATS if c != "meble" and in_cat(p, CATS[c][2])) or "Meble"
    return {
        "name": p["name"],
        "img": p["img"],
        "imgs": p.get("imgs") or [p["img"]],
        "desc": p.get("desc") or [],
        "catSlug": pc,
        "catTitle": CATS[pc][0],
        "catsMeta": cats_meta,
        "outlet": "outlet" in p["cats"],
        "rel": [q["slug"] for q in cat_products[pc] if q["url"] != p["url"]][:4],
    }
prod_index = {p["slug"]: product_data(p) for p in products}
json.dump(prod_index, open(os.path.join(SITE, "products.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
# Also as a JS global so product pages work over file:// (fetch is blocked there).
open(os.path.join(SITE, "products-data.js"), "w", encoding="utf-8").write(
    "window.PRODUCTS=" + json.dumps(prod_index, ensure_ascii=False, separators=(",", ":")) + ";")

product_shell = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Produkt — Domokoncept, salon meblowy Szczecin. Oferta na zapytanie." />
  <title>Produkt — Domokoncept</title>
  <link rel="icon" href="images/logo.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v=4" />
</head>
<body>
  <div class="cursor" data-cursor aria-hidden="true"><div class="cursor__dot"></div><div class="cursor__ring"></div></div>
  <div class="progress" data-progress aria-hidden="true"></div>
{header("sklep")}
  <main class="subpage" id="product-root"></main>
{FOOTER}
  <script src="main.js"></script>
  <script src="shop.js"></script>
  <script src="products-data.js"></script>
  <script src="product.js"></script>
</body>
</html>
'''
open(os.path.join(SITE, "product.html"), "w", encoding="utf-8").write(product_shell)

# ---------------- category + arrangement + landings ----------------
for slug, (title, sub, _) in CATS.items():
    listing_page(f"k-{slug}.html", title, sub, cat_products[slug],
                 f'<a href="sklep.html">Sklep</a> <span>/</span> {esc(title)}', "sklep",
                 f"{title} — Domokoncept Szczecin. {sub}.")
for slug, (title, sub, img) in ROOMS.items():
    listing_page(f"a-{slug}.html", f"Aranżacja: {title}", sub, room_products[slug],
                 f'<a href="aranzacje.html">Aranżacje</a> <span>/</span> {esc(title)}', "aranzacje",
                 f"Gotowa aranżacja {title} — Domokoncept Szczecin.")

def tile(href, title, sub, img):
    return f'''      <a href="{href}" class="card" data-reveal data-cursor-hover>
        <div class="card__media"><img loading="lazy" src="{esc(img)}" alt="{esc(title)}" /></div>
        <div class="card__body"><h3>{esc(title)}</h3><p>{esc(sub)}</p><span class="card__link">Zobacz →</span></div>
      </a>'''
tiles = "\n".join(tile(f"k-{c}.html", t, s, cat_products[c][0]["img"] if cat_products[c] else "") for c,(t,s,_) in CATS.items())
open(os.path.join(SITE,"sklep.html"),"w",encoding="utf-8").write(page("Sklep","sklep",
    page_hero("Sklep","Sklep",f"Wszystkie kategorie mebli i dodatków — {len(products)} produktów")+
    f'\n    <section class="section section--flush"><div class="container"><div class="cards cards--tiles">\n{tiles}\n</div></div></section>',
    "Sklep meblowy Domokoncept Szczecin — sofy, stoły, krzesła, oświetlenie i więcej."))
atiles = "\n".join(tile(f"a-{r}.html", t, s, img) for r,(t,s,img) in ROOMS.items())
open(os.path.join(SITE,"aranzacje.html"),"w",encoding="utf-8").write(page("Gotowe aranżacje","aranzacje",
    page_hero("Aranżacje","Gotowe aranżacje","Zobacz meble w naturalnych wnętrzach — pokój po pokoju")+
    f'\n    <section class="section section--flush"><div class="container"><div class="cards cards--tiles">\n{atiles}\n</div></div></section>',
    "Gotowe aranżacje wnętrz — sypialnia, salon, jadalnia, przedpokój."))

# ---------------- content pages ----------------
def write(fname, title, active, body, desc):
    open(os.path.join(SITE, fname), "w", encoding="utf-8").write(page(title, active, body, desc))

onas_body = page_hero("O nas", "Więcej niż salon meblowy", "…inna strona wnętrza — Szczecin") + f'''
    <section class="story">
      <div class="container story__grid">
        <div class="story__media" style="background-image:url('images/story.jpg')"></div>
        <div class="story__text">
          <p class="eyebrow" data-reveal>Dzień dobry</p>
          <h2 class="section__title" data-reveal>Rozgość się<br>w Domokoncept</h2>
          <p data-reveal>Powstaliśmy z myślą o tym, żeby być czymś więcej niż zwykłym salonem meblowym. Chcemy, żebyś poczuł się u nas jak w domu — usiądź na sofie, napij się dobrej kawy i bez pośpiechu wybierz razem z nami stół, łóżko czy fotel.</p>
          <p data-reveal>Nie urządzamy się jak typowy sklep. Meble prezentujemy w naturalnych aranżacjach, w których widać, jak naprawdę wyglądają w salonie, sypialni czy jadalni. Stawiamy na sprawdzony polski i skandynawski design, który służy przez lata.</p>
          <div class="stats" data-reveal>
            <div class="stat"><strong data-count="{len(products)}">0</strong><span>produktów</span></div>
            <div class="stat"><strong data-count="9">0</strong><span>marek premium</span></div>
            <div class="stat"><strong data-count="5">0</strong><span>min od centrum</span></div>
          </div>
        </div>
      </div>
    </section>
    <section class="section section--tint"><div class="container">
      <header class="section__head"><p class="eyebrow" data-reveal>Co nas wyróżnia</p><h2 class="section__title" data-reveal>Zakupy bez pośpiechu</h2></header>
      <div class="cards cards--tiles">
        <div class="feature" data-reveal><h3>Kawa i spokój</h3><p>Zapraszamy na kawę i czas na decyzję. U nas ogląda się meble na luzie, a nie w biegu między regałami.</p></div>
        <div class="feature" data-reveal><h3>Naturalne aranżacje</h3><p>Meble stoją w gotowych wnętrzach — widzisz kolor, materiał i skalę, zanim trafią do Ciebie do domu.</p></div>
        <div class="feature" data-reveal><h3>Wyselekcjonowane marki</h3><p>Vilmers, SITS, Comforty, Flexlux, Selfia, Take me home, Szyszka, Tamm room, FAMEG.</p></div>
      </div>
    </div></section>
    <section class="cta"><div class="container cta__inner">
      <h2 class="cta__title" data-reveal>Odwiedź nas w Szczecinie</h2>
      <p data-reveal>Niespełna 5 minut od centrum. Wpadnij na kawę i zobacz meble na żywo.</p>
      <div class="hero__cta" data-reveal style="justify-content:center;margin-top:28px">
        <a href="kontakt.html" class="btn" data-cursor-hover>Dane kontaktowe</a>
        <a href="sklep.html" class="btn btn--ghost" data-cursor-hover>Przeglądaj sklep</a>
      </div>
    </div></section>'''
write("o-nas.html", "O nas", "o-nas", onas_body, "O salonie Domokoncept w Szczecinie — więcej niż salon meblowy.")

kontakt_body = page_hero("Kontakt", "Kontakt", "Zadzwoń, napisz albo po prostu wpadnij na kawę") + '''
    <section class="section section--flush"><div class="container contact-grid">
      <div class="contact-info">
        <div class="contact-block" data-reveal><h4>Telefon</h4><a href="tel:+48511891500">+48 511 891 500</a></div>
        <div class="contact-block" data-reveal><h4>E-mail</h4><a href="mailto:salon@domokoncept.pl">salon@domokoncept.pl</a></div>
        <div class="contact-block" data-reveal><h4>Instagram</h4><a href="https://instagram.com/domokoncept" target="_blank" rel="noopener">@domokoncept</a></div>
        <div class="contact-block" data-reveal><h4>Salon</h4><p>Szczecin · niespełna 5 minut od centrum</p></div>
        <div class="contact-block" data-reveal><h4>Godziny otwarcia</h4>
          <ul class="hours">
            <li><span>Pon</span><span>12:00 – 17:00</span></li>
            <li><span>Wt – Pt</span><span>10:30 – 17:00</span></li>
            <li><span>Sob</span><span>10:00 – 14:00</span></li>
            <li><span>Niedz</span><span>nieczynne</span></li>
          </ul>
        </div>
      </div>
      <div class="contact-map" data-reveal>
        <iframe title="Mapa dojazdu do Domokoncept" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=Domokoncept%20Szczecin&output=embed"></iframe>
      </div>
    </div></section>'''
write("kontakt.html", "Kontakt", "kontakt", kontakt_body, "Kontakt — Domokoncept salon meblowy Szczecin. Telefon, e-mail, godziny otwarcia.")

comfino_body = page_hero("Raty Comfino", "Raty 0% z Comfino", "Kup wymarzone meble i rozłóż płatność na wygodne raty") + '''
    <section class="section section--flush"><div class="container prose">
      <p data-reveal>W Domokoncept zapłacisz za meble wygodnie — także na raty. Współpracujemy z <strong>Comfino</strong>, dzięki czemu decyzję o finansowaniu podejmiesz online, w kilka minut, bez wychodzenia z domu.</p>
      <div class="steps">
        <div class="step" data-reveal><span class="step__n">1</span><h3>Wybierz meble</h3><p>Przejrzyj sklep albo dogadaj szczegóły z nami w salonie.</p></div>
        <div class="step" data-reveal><span class="step__n">2</span><h3>Wybierz raty Comfino</h3><p>Przy zamówieniu zaznacz finansowanie Comfino i wybierz liczbę rat.</p></div>
        <div class="step" data-reveal><span class="step__n">3</span><h3>Gotowe</h3><p>Szybka decyzja online. Meble jadą do Ciebie, płatność rozłożona w czasie.</p></div>
      </div>
      <p class="prose__note" data-reveal>Szczegóły oferty, dostępne okresy i warunki finansowania potwierdzisz podczas zakupu oraz u obsługi salonu.</p>
      <div class="hero__cta" data-reveal><a href="sklep.html" class="btn" data-cursor-hover>Przeglądaj sklep</a><a href="kontakt.html" class="btn btn--ghost" data-cursor-hover>Zapytaj o raty</a></div>
    </div></section>'''
write("comfino.html", "Raty Comfino", "", comfino_body, "Raty 0% z Comfino — sfinansuj meble z Domokoncept wygodnie i online.")

BRAND_INFO = [
    ("Vilmers","Sofy, narożniki i łóżka łączące klasykę z nowoczesnością."),
    ("SITS","Skandynawskie sofy i fotele — komfort, tkaniny i modułowość."),
    ("Comforty","Ikony polskiego designu — sofy, krzesła i łóżka z charakterem."),
    ("Flexlux","Duński design siedzisk premium z dbałością o ergonomię."),
    ("Selfia","Drewniane stoły i szafki RTV, w tym rozkładany model LEVEL."),
    ("Take me home","Stoły, krzesła, komody, konsole, regały i łóżka."),
    ("Szyszka","Autorskie stoły, krzesła, hokery, szafki, regały i łóżka."),
    ("Tamm room","Stoły, krzesła, szafki, komody, konsole i łóżka."),
    ("FAMEG","Legendarne gięte krzesła i stoły, produkowane w Polsce od 1881 r."),
]
marki_body = page_hero("Marki", "Marki, które kochamy", "Sprawdzony polski i skandynawski design — starannie wybrany dla Ciebie") + \
    '\n    <section class="section section--flush"><div class="container"><div class="brand-grid">\n' + \
    "\n".join(f'      <div class="brand" data-reveal><h3>{esc(n)}</h3><p>{esc(d)}</p></div>' for n,d in BRAND_INFO) + \
    '\n</div></div></section>'
write("marki.html", "Marki", "marki", marki_body, "Marki w Domokoncept — Vilmers, SITS, Comforty, Flexlux, Selfia, Take me home, Szyszka, Tamm room, FAMEG.")

pomoc_body = page_hero("Pomoc", "Pomoc i najczęstsze pytania", "Dostawa, raty, zwroty i kontakt — w jednym miejscu") + '''
    <section class="section section--flush"><div class="container prose">
      <div class="faq" data-reveal><h3>Jak kupię meble?</h3><p>Wybierz produkty w sklepie i skontaktuj się z nami — telefonicznie, mailowo albo w salonie. Pomożemy dobrać wersję, tkaninę i wymiary oraz ustalić dostawę.</p></div>
      <div class="faq" data-reveal><h3>Czy mogę kupić na raty?</h3><p>Tak, oferujemy raty 0% z Comfino. Decyzję podejmiesz online w kilka minut. Szczegóły znajdziesz na stronie <a href="comfino.html">Raty Comfino</a>.</p></div>
      <div class="faq" data-reveal><h3>Jak wygląda dostawa?</h3><p>Realizujemy dostawę mebli, w tym na terenie Szczecina i okolic. Termin i koszt potwierdzamy indywidualnie przy zamówieniu.</p></div>
      <div class="faq" data-reveal><h3>Czy mogę zobaczyć meble na żywo?</h3><p>Oczywiście — zapraszamy do salonu w Szczecinie, niespełna 5 minut od centrum. Przygotujemy kawę i pokażemy meble w aranżacjach.</p></div>
      <div class="faq" data-reveal><h3>Zwroty i reklamacje</h3><p>W sprawach zwrotów, reklamacji i danych osobowych napisz na <a href="mailto:salon@domokoncept.pl">salon@domokoncept.pl</a> lub zadzwoń <a href="tel:+48511891500">+48 511 891 500</a>. Zasady opisuje <a href="regulamin.html">Regulamin</a>.</p></div>
      <div class="hero__cta" data-reveal><a href="kontakt.html" class="btn" data-cursor-hover>Kontakt</a><a href="sklep.html" class="btn btn--ghost" data-cursor-hover>Przeglądaj sklep</a></div>
    </div></section>'''
write("pomoc.html", "Pomoc", "", pomoc_body, "Pomoc — dostawa, raty, zwroty i kontakt. Domokoncept Szczecin.")

def legal(fname, title):
    body = page_hero(esc(title), title, "") + f'''
    <section class="section section--flush"><div class="container prose">
      <p data-reveal>Pełna, obowiązująca treść dokumentu „{esc(title)}” prowadzona jest przez salon Domokoncept. Uzupełnij tę stronę oficjalnym tekstem przed publikacją albo podlinkuj dokument z dotychczasowej strony.</p>
      <p data-reveal>W razie pytań dotyczących zakupów, zwrotów czy danych osobowych skontaktuj się z nami: <a href="mailto:salon@domokoncept.pl">salon@domokoncept.pl</a>, tel. <a href="tel:+48511891500">+48 511 891 500</a>.</p>
    </div></section>'''
    write(fname, title, "", body, f"{title} — Domokoncept Szczecin.")
legal("regulamin.html", "Regulamin")
legal("polityka-prywatnosci.html", "Polityka prywatności")

# ---------------- blog / baza wiedzy (one JSON + one dynamic template) ----------------
# Same approach as products: one articles.json + one article.html shell rendered
# client-side from ?a=<slug>, instead of ~40 static b-*.html files.
blog_path = os.path.join(HERE, "blog.json")
articles = json.load(open(blog_path, encoding="utf-8")) if os.path.exists(blog_path) else []
art_index = {a["slug"]: {"title": a["title"], "img": a.get("img", ""),
                         "excerpt": a.get("excerpt", ""), "paras": a.get("paras", [])}
             for a in articles}
json.dump(art_index, open(os.path.join(SITE, "articles.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
open(os.path.join(SITE, "articles-data.js"), "w", encoding="utf-8").write(
    "window.ARTICLES=" + json.dumps(art_index, ensure_ascii=False, separators=(",", ":")) + ";")

article_shell = f'''<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Baza wiedzy — Domokoncept, salon meblowy Szczecin." />
  <title>Baza wiedzy — Domokoncept</title>
  <link rel="icon" href="images/logo.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v=4" />
</head>
<body>
  <div class="cursor" data-cursor aria-hidden="true"><div class="cursor__dot"></div><div class="cursor__ring"></div></div>
  <div class="progress" data-progress aria-hidden="true"></div>
{header()}
  <main class="subpage" id="article-root"></main>
{FOOTER}
  <script src="main.js"></script>
  <script src="shop.js"></script>
  <script src="articles-data.js"></script>
  <script src="article.js"></script>
</body>
</html>
'''
open(os.path.join(SITE, "article.html"), "w", encoding="utf-8").write(article_shell)

# blog index
bcards = "".join(
    f'''      <a href="article.html?a={a['slug']}" class="card" data-reveal data-cursor-hover>
        <div class="card__media"><img loading="lazy" src="{esc(a['img'])}" alt="{esc(a['title'])}" /></div>
        <div class="card__body"><h3>{esc(a['title'])}</h3><p>{esc(a['excerpt'][:110])}…</p><span class="card__link">Czytaj →</span></div>
      </a>''' for a in articles)
blog_body = page_hero("Baza wiedzy", "Baza wiedzy", "Inspiracje, porady i trendy wnętrzarskie od Domokoncept") + \
    f'\n    <section class="section section--flush"><div class="container"><div class="cards cards--tiles">\n{bcards}\n</div></div></section>'
write("blog.html", "Baza wiedzy", "", blog_body, "Baza wiedzy Domokoncept — inspiracje i porady wnętrzarskie.")

print("product pages:", len(products), "| blog articles:", len(articles))
print("category pages:", len(CATS), "arrangement pages:", len(ROOMS))
for c in CATS: print(f"  {c:16}{len(cat_products[c])}")
