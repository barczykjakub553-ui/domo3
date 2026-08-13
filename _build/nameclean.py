#!/usr/bin/env python3
"""Shared: brand inference + pretty product-name builder.
Used by apply_products.py (one-shot) and generate.py (rebuild)."""
import re

# Canonical brand labels as shown on domokoncept.pl, keyed by tokens that may
# appear in a product name or slug when the scraped "Marka:" line was missing.
BRAND_HINTS = [
    ("loftdecora", "LoftDecora"), ("loftowy", "LoftDecora"), ("grop", "LoftDecora"),
    ("comforty", "Com40 / Comforty"), ("com40", "Com40 / Comforty"),
    ("fargotex", "Fargotex"), ("magic home", "Fargotex"),
    ("sits", "SITS"), ("vilmers", "Vilmers"), ("flexlux", "Flexlux"),
    ("fameg", "Fameg"), ("paged", "Paged"), ("selfia", "Selfia"),
    ("take me home", "Take Me Home"), ("take-me-home", "Take Me Home"),
    ("szyszka", "Szyszka"), ("misaform", "MisaForm"), ("vzor", "Vzor"),
]

def infer_brand(name, slug):
    hay = (name + " " + slug).lower()
    for tok, label in BRAND_HINTS:
        if tok in hay:
            return label
    return None

# --- name cleaning ---------------------------------------------------------
# Type keyword -> canonical "Rodzaj". Longer/ambiguous keys first so "stolik"
# wins over "stół", "narożnik" maps to Sofa, etc.
TYPES = [
    ("szafka rtv", "Szafka RTV"),
    ("narożnik", "Sofa"), ("naroznik", "Sofa"),
    ("stolik", "Stolik"),
    ("sofa", "Sofa"),
    ("fotel", "Fotel"),
    ("krzesło", "Krzesło"), ("krzeslo", "Krzesło"),
    ("hoker", "Hoker"), ("taboret", "Taboret"),
    ("stół", "Stół"), ("stol", "Stół"),
    ("komoda", "Komoda"), ("szafka", "Szafka"),
    ("regał", "Regał"), ("regal", "Regał"),
    ("biurko", "Biurko"),
    ("łóżko", "Łóżko"), ("lozko", "Łóżko"),
    ("konsola", "Konsola"),
    ("podnóżek", "Podnóżek"), ("podnozek", "Podnóżek"), ("pufa", "Pufa"),
    ("wieszak", "Wieszak"),
    ("żyrandol", "Żyrandol"), ("kinkiet", "Kinkiet"), ("lampa", "Lampa"),
    ("dywan", "Dywan"),
    ("ławka", "Ławka"), ("lawka", "Ławka"), ("ława", "Ława"),
    ("lustro", "Lustro"), ("tacka", "Tacka"),
    ("półka", "Półka"), ("polka", "Półka"),
]
CAT_TYPE = {
    "sofy": "Sofa", "sofy-modulowe": "Sofa", "fotele": "Fotel", "krzesla": "Krzesło",
    "stoly": "Stół", "stoliki": "Stolik", "hokery": "Hoker", "komody": "Komoda",
    "dywany": "Dywan", "oswietlenie": "Lampa",
}
# All type words to strip out of the model part.
TYPE_WORDS = sorted({k for k, _ in TYPES} | {"sofy"}, key=len, reverse=True)
# Store noise + descriptive attributes that shouldn't be in a tidy shop name.
NOISE = [
    "domokoncept", "konfiguracja w domokoncept", "próbki w domokoncept",
    "z funkcją spania", "z otomaną", "z podnóżkiem", "z szufladą", "z szuflada",
    "do jadalni", "do salonu", "do sypialni", "do książek", "do salonu",
    "nogi tapicerowane", "dekoracja ścienna", "magic home", "stone collection",
    "narożna", "narożny", "modułowa", "modułowy", "modulowa", "modulowy",
    "rozkładana", "rozkładany", "roskladany", "roskladana", "kawowy", "kawowa",
    "loftowy", "loftowa", "na nóżkach", "wisząca", "wiszący", "drewniany",
    "drewniana", "drewniane", "restauracyjny", "obrotowy", "premium", "lounge",
    "outlet", "sale", "poducha", "handmade", "kopia", "nocna", "ogrodowy",
    "ogrodowa", "młodzieżowa", "luksusowa", "nowoczesna", "nowoczesny",
    "jadalniany", "jadalniana", "jadalniane",
    # room-scene prefixes used by showcase listings
    "salon", "jadalnia", "sypialnia", "przedpokój", "przedpokoj",
    "aranżacja", "aranzacja", "aranżacje", "mieszkanie",
]

def _brand_words(brand):
    if not brand:
        return []
    return [w for w in re.split(r"[^\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+", brand) if len(w) > 1]

def detect_type(name, cat_slug):
    low = name.lower()
    for key, canon in TYPES:
        if key in low:
            return canon
    return CAT_TYPE.get(cat_slug, "")

def _rm(text, phrases):
    for p in sorted(phrases, key=len, reverse=True):
        text = re.sub(r"(?<![\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ])" + re.escape(p) +
                      r"(?![\wąćęłńóśźżĄĆĘŁŃÓŚŹŻ])", " ", text, flags=re.I)
    return text

def clean_name(name, brand, cat_slug):
    typ = detect_type(name, cat_slug)
    s = name.split("|")[0]                       # drop marketing tail after |
    # model sits before a spaced dash separator; hyphens inside codes (B-1403) stay
    s = re.split(r"\s+[–—-]\s+", s)[0]
    s = _rm(s, _brand_words(brand) + NOISE + TYPE_WORDS)
    model = re.sub(r"\s+", " ", s).strip(" -–,·")
    if len(model) <= 1:                 # over-stripped (e.g. room-scene) -> keep original
        return name.strip()
    if model.islower():
        model = model.title()
    out = (typ + " " + model).strip() if typ else model
    return re.sub(r"\s+", " ", out).strip()
