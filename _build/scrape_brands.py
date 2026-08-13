#!/usr/bin/env python3
"""Scrape the WooCommerce brand ("Marka:" / "Producent:") for every product.
Reads products.json (urls), writes brands.json = {slug: "Brand" | null}."""
import re, json, html, urllib.request, os, sys, threading
import concurrent.futures as cf

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) domokoncept-mirror/1.0"}
prods = json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))

def slug_of(url): return url.rstrip("/").split("/")[-1]
# "Marka:" line (fallback "Producent:") holds the per-product brand anchors.
MARKA = re.compile(r'(?:Marka|Producent):\s*(.*?)</span>', re.S)
ANCHOR = re.compile(r'/marka/[^"]+/"[^>]*>([^<]+)</a>')

def get(url):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")
        except Exception:
            pass
    return ""

def brand_of(h):
    m = MARKA.search(h)
    if not m: return None
    names = [html.unescape(x).strip() for x in ANCHOR.findall(m.group(1))]
    return " / ".join(dict.fromkeys(names)) or None

out = {}; done = [0]; lock = threading.Lock()
def work(p):
    b = brand_of(get(p["url"]))
    with lock:
        out[slug_of(p["url"])] = b
        done[0] += 1
        if done[0] % 50 == 0: print(f"  {done[0]}/{len(prods)}", file=sys.stderr)

with cf.ThreadPoolExecutor(max_workers=12) as ex:
    list(ex.map(work, prods))

json.dump(out, open(os.path.join(HERE, "brands.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
miss = [s for s, b in out.items() if not b]
print("TOTAL", len(out), "| with brand:", sum(1 for b in out.values() if b), "| missing:", len(miss))
from collections import Counter
for b, n in Counter(v for v in out.values() if v).most_common(): print(f"  {n:4}  {b}")
