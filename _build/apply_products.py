#!/usr/bin/env python3
"""Enrich site/products.json: add `brand`, tidy `name`, drop Aris Concept.
Dry-run by default (prints report + writes name_review.tsv); pass --apply to write."""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "site")
sys.path.insert(0, HERE)
from nameclean import clean_name, infer_brand

APPLY = "--apply" in sys.argv
prods = json.load(open(os.path.join(SITE, "products.json"), encoding="utf-8"))
brands = json.load(open(os.path.join(HERE, "brands.json"), encoding="utf-8"))

# 1) resolve brand: scraped -> inferred from name/slug
for slug, p in prods.items():
    p["brand"] = brands.get(slug) or infer_brand(p["name"], slug)

# 2) Aris Concept set: authoritative brand match, plus image-URL fallback for the
#    handful whose product page predates the scrape (img filename carries "aris").
def _img_aris(p):
    for u in [p.get("img", "")] + p.get("imgs", []):
        u = (u or "").lower()
        if "aris" in u and "paris" not in u:
            return True
    return False
aris = {s for s, p in prods.items()
        if (p.get("brand") or "").lower().startswith("aris") or _img_aris(p)}
print(f"Aris Concept to remove: {len(aris)}")

# 3) drop them + strip from rel[]
for s in aris:
    prods.pop(s, None)
for p in prods.values():
    if "rel" in p:
        p["rel"] = [r for r in p["rel"] if r not in aris]

# 4) tidy names
changes = []
for slug, p in prods.items():
    old = p["name"]
    new = clean_name(old, p.get("brand"), p.get("catSlug", ""))
    if new != old:
        changes.append((slug, old, new, p.get("brand")))
    p["name"] = new

miss = [(s, p["name"]) for s, p in prods.items() if not p.get("brand")]
print(f"products now: {len(prods)} | renamed: {len(changes)} | still no brand: {len(miss)}")

# review file
with open(os.path.join(HERE, "name_review.tsv"), "w", encoding="utf-8") as f:
    f.write("slug\tbrand\told\tnew\n")
    for slug, old, new, br in sorted(changes, key=lambda x: x[2]):
        f.write(f"{slug}\t{br}\t{old}\t{new}\n")

print("\n--- rename sample (varied) ---")
for slug, old, new, br in changes[::max(1, len(changes)//30)][:30]:
    print(f"  [{(br or '—')[:16]:16}] {old[:42]:42} -> {new}")

print("\n--- still missing brand (all) ---")
for s, n in miss:
    print(f"  {s:42} {n}")

if APPLY:
    # site products.json (minified, matches original) + JS global
    json.dump(prods, open(os.path.join(SITE, "products.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    open(os.path.join(SITE, "products-data.js"), "w", encoding="utf-8").write(
        "window.PRODUCTS=" + json.dumps(prods, ensure_ascii=False, separators=(",", ":")) + ";")
    # remove Aris product cards from static catalog pages
    card = re.compile(r'\n[ \t]*<a class="product product--link" href="product\.html\?p=(?P<s>[^"&]+)"[^>]*>.*?</a>', re.S)
    tot = 0
    for fp in glob.glob(os.path.join(SITE, "*.html")):
        t = open(fp, encoding="utf-8").read()
        new = card.sub(lambda m: "" if m.group("s") in aris else m.group(0), t)
        if new != t:
            open(fp, "w", encoding="utf-8").write(new)
            tot += len(card.findall(t)) - len(card.findall(new))
    print(f"\nAPPLIED. Aris cards removed from html: {tot}")
else:
    print("\n(dry-run — nothing written except name_review.tsv; add --apply to write)")
