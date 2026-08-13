#!/usr/bin/env python3
"""Stage 2: fetch every product page -> gallery images + description.
Reads products.json, writes products_full.json (adds imgs[], desc[])."""
import re, json, html, urllib.request, concurrent.futures as cf, sys, os, threading
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) domokoncept-mirror/1.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
prods = json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))

def get(url):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")
        except Exception:
            pass
    return ""

H1 = re.compile(r'<h1[^>]*class="product_title[^"]*"[^>]*>(.*?)</h1>', re.S)
PRICE = re.compile(r'<p class="price">(.*?)</p>', re.S)
LARGE = re.compile(r'data-large_image="([^"]+)"')
SHORT = re.compile(r'woocommerce-product-details__short-description">(.*?)</div>', re.S)
DESCTAB = re.compile(r'woocommerce-Tabs-panel--description"[^>]*>(.*?)</div>\s*<div', re.S)
TAGP = re.compile(r'</p>|<br\s*/?>|</li>', re.I)
STRIP = re.compile(r'<[^>]+>')
def txt(s): return html.unescape(STRIP.sub('', s)).strip()

def paras(block):
    if not block: return []
    out = []
    for chunk in TAGP.split(block):
        t = re.sub(r'\s+', ' ', txt(chunk)).strip()
        if len(t) > 1:
            out.append(t)
    return out

done = [0]; lock = threading.Lock()
def enrich(p):
    h = get(p["url"])
    imgs = []
    if h:
        for u in LARGE.findall(h):
            u = html.unescape(u)
            if u.startswith('{{') or u.startswith('data:') or u in imgs: continue
            imgs.append(u)
        m = SHORT.search(h) or DESCTAB.search(h)
        p["desc"] = paras(m.group(1)) if m else []
    p["imgs"] = imgs or ([p["img"]] if p.get("img") else [])
    with lock:
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  {done[0]}/{len(prods)}", file=sys.stderr)
    return p

with cf.ThreadPoolExecutor(max_workers=12) as ex:
    prods = list(ex.map(enrich, prods))

json.dump(prods, open(os.path.join(HERE, "products_full.json"), "w", encoding="utf-8"), ensure_ascii=False)
img_counts = [len(p["imgs"]) for p in prods]
print("TOTAL", len(prods))
print("with >=1 gallery img:", sum(1 for p in prods if p["imgs"]))
print("with multi-img gallery:", sum(1 for c in img_counts if c > 1))
print("with description:", sum(1 for p in prods if p.get("desc")))
print("avg imgs:", round(sum(img_counts)/len(img_counts), 1), "max:", max(img_counts))
