#!/usr/bin/env python3
"""Validator for MOBILIUS AirPods case listings (Amazon US).

Rules come from SEO-Rules.md. Every limit below is tagged with its status there.
Usage:
    python3 seo_check.py listing.json
    python3 seo_check.py --batch listings.json   (adds Color/title uniqueness per parent)
    python3 seo_check.py --selftest
listing.json = {"title": str, "highlight": str, "bullets": [str x5],
                "description": str, "backend": str, "series": "pro" | "airpods4"}
Exit code 0 = no errors (warnings allowed), 1 = at least one error.
"""
import json
import re
import sys
from collections import Counter

TITLE_MAX = 75              # Amazon announcement 2026-06-10, brand counts (user decision)
HIGHLIGHT_MAX = 125         # Amazon announcement
BULLET_MAX = 500            # user decision (Amazon staff: 500 per bullet recommended)
BULLET_PRIORITY_BYTES = 1000  # user decision: priority keywords inside first 1000 bytes of 5 bullets
DESC_MAX = 2000             # widely stated, no Amazon-staff source found (OPEN)
BACKEND_MAX_BYTES = 249     # Amazon staff (Cooper_Amazon), "Keyword attributes explained"
BACKEND_TARGET_BYTES = 240  # safety margin below 249

TITLE_FORBIDDEN_CHARS = set("!$?_{}^¬¦")
PROMO = ["free shipping", "100% quality", "guarantee", "best seller", "best-seller",
         "sale", "discount", "limited time", "new arrival", "hot"]
# "no claims at all" (user decision) + Amazon prohibited claims list
CLAIMS = ["antimicrobial", "anti-microbial", "antibacterial", "anti-bacterial", "shockproof",
          "shock-proof", "shock absorbing", "waterproof", "water-proof", "water resistant",
          "dustproof", "dust-proof", "dust proof", "drop test", "drop-tested", "military",
          "scratch-proof", "scratchproof", "scratch resistant", "anti-scratch", "anti-slip",
          "magsafe", "wireless charging", "qi ", "eco-friendly", "environmentally friendly",
          "premium", "best", "perfect", "ultimate", "durable", "unbreakable", "indestructible",
          "full protection", "360", "guarantee", "refund", "warranty", "skin-friendly",
          "bamboo", "soy", "pro 3", "3rd generation", "airpods pro 3",
          "lightweight", "slim", "scratches", "bumps", "full access", "precise cut"]
# print q230 looks like a known animated character: describe it only by colors and shapes (user decision)
Q230_FORBIDDEN = ["scientist", "potion", "lab coat", "laboratory", "rick", "morty", "mad ", "goggles"]
ABBREV = ["qty", "pkg", "w/", "approx.", "approx ", "pcs", "w/o"]
PLACEHOLDERS = ["n/a", "tbd", "not applicable", "copy pending", "to be decided"]
ASIN_RE = re.compile(r"\bB0[A-Z0-9]{8}\b")
SPELLED = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
           "6": "six", "7": "seven", "8": "eight", "9": "nine"}
# digits that are allowed because they are model names / measurements
NUM_OK_CONTEXT = re.compile(
    r"(airpods?\s*(pro\s*)?\d|pro\s*\d|\d(st|nd|rd|th)\b|\d(\.\d+)?\s*mm\b|\d\s*/\s*\d|\(\s*\d)",
    re.I)
STOPWORDS = {"for", "and", "with", "the", "a", "an", "of", "to", "in", "on", "or"}


def nbytes(s):
    return len(s.encode("utf-8"))


def check(listing):
    errs, warns = [], []
    t = listing.get("title", "")
    h = listing.get("highlight", "")
    bl = listing.get("bullets", [])
    d = listing.get("description", "")
    b = listing.get("backend", "")
    series = listing.get("series", "")

    # ---- title
    if not t:
        errs.append("title: empty")
    if len(t) > TITLE_MAX:
        errs.append(f"title: {len(t)} chars > {TITLE_MAX} (brand counts)")
    if not t.startswith("MOBILIUS"):
        errs.append("title: must start with brand MOBILIUS")
    bad = sorted(set(t) & TITLE_FORBIDDEN_CHARS)
    if bad:
        errs.append(f"title: forbidden characters {bad}")
    if any(ord(c) > 127 for c in t + h + d + b + "".join(bl)):
        errs.append("non-ASCII character found (no emojis, ®, ™, ©, accents; template: no high ASCII)")
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9']+", t)]
    for w, n in Counter(words).items():
        if n > 2 and w not in STOPWORDS:
            errs.append(f"title: word '{w}' used {n} times (max 2)")
    low = t.lower()
    for p in PROMO:
        if re.search(rf"\b{re.escape(p)}\b", low):
            errs.append(f"title: promotional phrase '{p}'")
    if t.isupper():
        errs.append("title: ALL CAPS")

    # ---- highlight
    if len(h) > HIGHLIGHT_MAX:
        errs.append(f"highlight: {len(h)} chars > {HIGHLIGHT_MAX}")
    if h.endswith("."):
        warns.append("highlight: ends with a period (use phrases, not a sentence)")
    tw = set(words) - STOPWORDS
    hw = [w.lower() for w in re.findall(r"[A-Za-z0-9']+", h)]
    rep = sorted({w for w in hw if w in tw and w not in {"airpods", "pro", "case", "generation"}})
    if rep:
        warns.append(f"highlight: repeats title words {rep} (template: do not repeat title info)")

    # ---- bullets
    if len(bl) != 5:
        errs.append(f"bullets: {len(bl)} found, need 5")
    total = 0
    for i, x in enumerate(bl, 1):
        n = len(x)
        total += nbytes(x)
        if n > BULLET_MAX:
            errs.append(f"bullet {i}: {n} chars > {BULLET_MAX}")
        if n < 10:
            errs.append(f"bullet {i}: shorter than 10 chars")
        if x and not x[0].isupper():
            errs.append(f"bullet {i}: must start with a capital letter")
        if x.rstrip().endswith((".", "!", ";", ",")):
            errs.append(f"bullet {i}: no end punctuation allowed")
        if ":" not in x[:60]:
            warns.append(f"bullet {i}: no 'Header: description' structure in first 60 chars")
        letters = re.sub(r"[^A-Za-z ]", "", ASIN_RE.sub(" ", x))
        for w in letters.split():
            if len(w) > 3 and w.isupper() and w not in {"TPU", "USB"}:
                errs.append(f"bullet {i}: ALL CAPS word '{w}'")
        for a in ABBREV:
            if a in x.lower():
                errs.append(f"bullet {i}: abbreviation '{a.strip()}'")
        if ASIN_RE.search(x):
            errs.append(f"bullet {i}: contains ASIN")
        for ph in PLACEHOLDERS:
            if ph in x.lower():
                errs.append(f"bullet {i}: placeholder text '{ph}'")
        for m in re.finditer(r"(?<![\w.])([1-9])(?![\w.%])", x):
            ctx = x[max(0, m.start() - 12):m.end() + 12]
            if not NUM_OK_CONTEXT.search(ctx):
                warns.append(f"bullet {i}: digit {m.group(1)} should be spelled '{SPELLED[m.group(1)]}' (unless model/measurement)")
        if re.search(r"\d(mm|cm|in|g|oz)\b", x):
            errs.append(f"bullet {i}: missing space between number and unit")
    if total > BULLET_PRIORITY_BYTES:
        warns.append(f"bullets: total {total} bytes; only the first {BULLET_PRIORITY_BYTES} bytes are assumed indexed. "
                     f"Priority keywords must sit inside them")
    joined = " ".join(bl)

    # ---- description
    if len(d) > DESC_MAX:
        errs.append(f"description: {len(d)} chars > {DESC_MAX}")
    if re.search(r"<[^>]+>", d):
        errs.append("description: HTML tags not allowed (template + Amazon announcement)")
    if d.isupper():
        errs.append("description: ALL CAPS")

    # ---- backend
    nb = nbytes(b)
    if nb > BACKEND_MAX_BYTES:
        errs.append(f"backend: {nb} bytes > {BACKEND_MAX_BYTES}")
    elif nb > BACKEND_TARGET_BYTES:
        warns.append(f"backend: {nb} bytes, above safety target {BACKEND_TARGET_BYTES}")
    if re.search(r"[,;|]", b):
        errs.append("backend: use spaces only, no commas or semicolons")
    if b != b.lower():
        warns.append("backend: use lowercase")
    bw = b.lower().split()
    dup = sorted(w for w, n in Counter(bw).items() if n > 1)
    if dup:
        errs.append(f"backend: repeated words {dup}")
    visible = set(re.findall(r"[a-z0-9]+", (t + " " + h + " " + joined + " " + d).lower()))
    inv = sorted(w for w in bw if w in visible)
    if inv:
        warns.append(f"backend: words already visible in title/bullets/description: {inv}")
    if ASIN_RE.search(b.upper()):
        errs.append("backend: contains ASIN")
    if re.search(r"\b(apple|samsung|esr|spigen|caseology|ljusmicker)\b", b.lower()):
        errs.append("backend: brand names not allowed")

    # ---- claims, all fields
    blob = " ".join([t, h, joined, d, b]).lower() + " "
    for c in CLAIMS:
        if c in blob:
            errs.append(f"claim/forbidden term '{c.strip()}' found (no-claims policy)")

    # ---- size and weight only in feed fields (user decision)
    if re.search(r"\b(64|48|25|74|58|35)\s*mm\b|\b(30|40)\s*(g|grams?)\b", blob):
        errs.append("size or weight numbers must stay in feed fields, not in text (AirPods 4 uses an average size)")

    # ---- print-specific rules
    if str(listing.get("sku", "")).endswith("q230"):
        for w in Q230_FORBIDDEN:
            if w in blob:
                errs.append(f"q230: '{w.strip()}' not allowed; describe the print only by colors and shapes")

    # ---- series-specific
    if series == "pro":
        if not re.search(r"1st", t + " " + h + " " + (bl[0] if bl else ""), re.I):
            errs.append("pro: Pro 1st generation must be named in title, highlight or bullet 1")
        if not re.search(r"(pro 2|2nd)", t + " " + h + " " + (bl[0] if bl else ""), re.I):
            errs.append("pro: Pro 2 / 2nd generation must be named in title, highlight or bullet 1")
        if re.search(r"airpods\s*(1|2)\s*/\s*(2|1)", blob):
            errs.append("pro: '1/2' without 'Pro 2nd/1st Generation' means AirPods 1/2 (wrong product)")
    if series == "airpods4":
        if not re.search(r"airpods\s*5", t, re.I) or not re.search(r"airpods\s*4", t, re.I):
            errs.append("airpods4: title must name both AirPods 5 and AirPods 4 (user: same case fits both)")
        first = t + " " + h + " " + (bl[0] if bl else "")
        if not (re.search(r"(airpods\s*4|4th)", first, re.I) and re.search(r"(airpods\s*5|5th)", first, re.I)):
            errs.append("airpods4: AirPods 4 and AirPods 5 must both be named in title, highlight or bullet 1")
        if re.search(r"\b(anc|noise cancel\w*)\b", blob):
            errs.append("airpods4: ANC fit not confirmed by user")
    if re.search(r"\b20(19|2\d)\b", blob):
        errs.append("release years are not confirmed by user: remove year numbers")
    if "carabiner" not in blob and "keychain" not in blob:
        warns.append("package: carabiner keychain (confirmed by user) not mentioned")
    return errs, warns


EXAMPLE = {
    "series": "pro",
    "title": "MOBILIUS TPU Case for AirPods Pro 2nd/1st Generation, Black Desert Stamps",
    "highlight": "Soft-Touch Coating, Two-Piece Design, Carabiner Included, Average 2.5 mm Thickness",
    "bullets": [
        "Compatibility: Case cover for Apple AirPods Pro 2nd generation and AirPods Pro 1st generation charging cases; one fit for both; earbuds and charging case not included",
        "TPU material: Made from TPU with a soft-touch coating; average wall thickness 2.5 mm",
        "Desert climbing stamp design: Black matte finish with a printed trio of stamps for a decorative look",
        "Two-piece design: Top and base parts cover the AirPods Pro charging case; cutout for the charging cable",
        "Carabiner included: One case and one carabiner in the package for attaching to a bag, backpack, or belt loop",
    ],
    "description": "MOBILIUS case cover for AirPods Pro 2nd generation and AirPods Pro 1st generation charging cases. Made from TPU with a soft-touch coating and an average thickness of 2.5 mm. The package contains one case and one carabiner. Earbuds and the charging case are not included.",
    "backend": "airpod airpodpro procase podspro",
}


def batch(path):
    """Batch file: {"listings": [{"sku","parent","color", ...single listing fields...}]}.
    Besides every single-listing check, Color and title must be unique inside one parent
    (variation theme COLOR: duplicate Color values prevent the variation from being created)."""
    data = json.load(open(path, encoding="utf-8"))["listings"]
    failed = 0
    by_parent = {}
    for L in data:
        errs, warns = check(L)
        by_parent.setdefault(L.get("parent", ""), []).append(L)
        for e in errs:
            print(f"ERROR   [{L.get('sku')}] {e}")
        for w in warns:
            print(f"WARNING [{L.get('sku')}] {w}")
        failed += bool(errs)
    for parent, items in by_parent.items():
        for field in ("color", "title"):
            seen = {}
            for L in items:
                v = re.sub(r"\s+", " ", L.get(field, "")).strip().lower()
                if not v:
                    print(f"ERROR   [{L.get('sku')}] {field}: empty")
                    failed += 1
                elif v in seen:
                    print(f"ERROR   [{L.get('sku')}] {field} duplicates [{seen[v]}] inside parent {parent}")
                    failed += 1
                else:
                    seen[v] = L.get("sku")
                if field == "color" and v and any(ord(c) > 127 for c in v):
                    print(f"ERROR   [{L.get('sku')}] color: non-ASCII")
                    failed += 1
    print(f"{len(data)} listings, {failed} failing checks")
    return 1 if failed else 0


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--batch":
        return batch(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        listing = EXAMPLE
    elif len(sys.argv) > 1:
        listing = json.load(open(sys.argv[1], encoding="utf-8"))
    else:
        print(__doc__)
        return 2
    errs, warns = check(listing)
    t = listing["title"]
    print(f"title {len(t)}/{TITLE_MAX} | highlight {len(listing['highlight'])}/{HIGHLIGHT_MAX} | "
          f"bullets {[len(x) for x in listing['bullets']]} chars, "
          f"{sum(nbytes(x) for x in listing['bullets'])} bytes | description {len(listing['description'])}/{DESC_MAX} | "
          f"backend {nbytes(listing['backend'])}/{BACKEND_MAX_BYTES} bytes")
    for e in errs:
        print("ERROR  ", e)
    for w in warns:
        print("WARNING", w)
    print("RESULT:", "FAIL" if errs else "PASS")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
