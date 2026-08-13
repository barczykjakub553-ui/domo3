#!/usr/bin/env python3
"""Stage 1: crawl /sklep/ (all products, cats in <li> class) + arrangements.
Writes _build/products.json = [{url,name,img,price,cats,rooms}]. Stdlib only."""
import re, json, html, urllib.request, concurrent.futures as cf, sys, os
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) domokoncept-mirror/1.0"}
BASE = "https://domokoncept.pl"
HERE = os.path.dirname(os.path.abspath(__file__))

def get(url):
    last = None
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")
        except Exception as e:
            last = e
    print("  ! fail", url, last, file=sys.stderr); return ""

LI = re.compile(r'<li[^>]*class="([^"]*\bproduct\b[^"]*)"[^>]*>(.*?)</li>', re.S)
HREF = re.compile(r'<a[^>]+href="([^"]+)"[^>]*class="[^"]*woocommerce-LoopProduct-link')
IMG = re.compile(r'<img[^>]+src="([^"]+)"'); SRCSET = re.compile(r'srcset="([^"]+)"')
TITLE = re.compile(r'woocommerce-loop-product__title">(.*?)</h2>', re.S)
PRICE = re.compile(r'<span class="price">(.*?)</span>\s*</a>', re.S)
BDI = re.compile(r'<bdi>(.*?)</bdi>', re.S); CATSLUG = re.compile(r'product_cat-([a-z0-9-]+)')
TAG = re.compile(r'<[^>]+>')
def clean(s): return html.unescape(TAG.sub('', s)).strip()

def pick_img(src, srcset):
    if srcset:
        best = None
        for part in srcset.split(','):
            b = part.strip().split(' ')
            if len(b) >= 2 and b[1] in ('600w', '768w'):
                best = b[0]
                if b[1] == '600w': break
        if best: return best
    return src

def parse(h):
    out = []
    for cls, body in LI.findall(h):
        hm, tm = HREF.search(body), TITLE.search(body)
        if not hm or not tm: continue
        im, sm = IMG.search(body), SRCSET.search(body)
        pm = PRICE.search(body); price = ''
        if pm:
            bd = BDI.findall(pm.group(1))
            price = ' – '.join(clean(b) for b in bd) if bd else clean(pm.group(1))
        out.append({"url": hm.group(1), "name": clean(tm.group(1)),
                    "img": pick_img(im.group(1) if im else '', sm.group(1) if sm else ''),
                    "price": price, "cats": sorted(set(CATSLUG.findall(cls)))})
    return out

def maxpage(h):
    ns = [int(n) for n in re.findall(r'page/(\d+)', h)]; return max(ns) if ns else 1
def crawl(base, pages):
    urls = [base] + [f"{base}page/{p}/" for p in range(2, pages + 1)]
    res = []
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(lambda u: parse(get(u)), urls): res.extend(r)
    return res

print("crawl /sklep/", file=sys.stderr)
p1 = get(f"{BASE}/sklep/"); mp = maxpage(p1); print(" pages", mp, file=sys.stderr)
allp = crawl(f"{BASE}/sklep/", mp)
by = {}
for p in allp:
    if p["url"] not in by:
        p["rooms"] = []; by[p["url"]] = p
    else:
        by[p["url"]]["cats"] = sorted(set(by[p["url"]]["cats"]) | set(p["cats"]))
print(" unique", len(by), file=sys.stderr)
for room in ["sypialnia", "salon", "jadalnia", "przedpokoj"]:
    u = f"{BASE}/produkty/gotowe-aranzacje/{room}/"; h = get(u)
    for p in crawl(u, maxpage(h)):
        t = by.get(p["url"])
        if not t:
            p["rooms"] = [room]; by[p["url"]] = p
        elif room not in t["rooms"]:
            t["rooms"].append(room)
    print(" room", room, file=sys.stderr)
json.dump(list(by.values()), open(os.path.join(HERE, "products.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("TOTAL", len(by))
