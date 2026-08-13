#!/usr/bin/env python3
"""Stage 3: scrape /baza-wiedzy/ articles -> blog.json (title,url,img,excerpt,paras)."""
import re, json, html, urllib.request, concurrent.futures as cf, os, sys
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) domokoncept-mirror/1.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
def get(u):
    for _ in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode("utf-8","replace")
        except Exception: pass
    return ""
sm = get("https://domokoncept.pl/post-sitemap.xml")
urls = [u for u in re.findall(r'<loc>([^<]+)</loc>', sm) if '/baza-wiedzy/' in u and u.rstrip('/').split('/')[-1] != 'baza-wiedzy']
print("articles:", len(urls), file=sys.stderr)
STRIP = re.compile(r'<[^>]+>')
def txt(s): return re.sub(r'\s+', ' ', html.unescape(STRIP.sub('', s))).strip()
def scrape(u):
    h = get(u)
    if not h: return None
    m = re.search(r'<h1[^>]*class="[^"]*entry-title[^"]*"[^>]*>(.*?)</h1>', h, re.S) or re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    title = txt(m.group(1)) if m else u.rstrip('/').split('/')[-1].replace('-', ' ').capitalize()
    im = re.search(r'<meta[^>]+og:image[^>]+content="([^"]+)"', h)
    img = html.unescape(im.group(1)) if im else ""
    mc = re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*?)(?:</article>|<footer|class="(?:post|entry)-(?:footer|nav|meta)|yarpp|related)', h, re.S) \
         or re.search(r'class="[^"]*entry-content[^"]*"[^>]*>(.*)', h, re.S)
    paras = []
    if mc:
        for chunk in re.split(r'</p>|</li>', mc.group(1)):
            t = txt(chunk)
            if len(t) > 40 and 'function' not in t.lower(): paras.append(t)
    return {"url": u, "slug": u.rstrip('/').split('/')[-1], "title": title, "img": img,
            "excerpt": paras[0][:200] if paras else "", "paras": paras[:20]}
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    arts = [a for a in ex.map(scrape, urls) if a and a["paras"]]
json.dump(arts, open(os.path.join(HERE, "blog.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("scraped:", len(arts), "| with img:", sum(1 for a in arts if a["img"]))
