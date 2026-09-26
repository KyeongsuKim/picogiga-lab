"""
Rebuild assets/js/publications.js from Google Scholar, OpenAlex and KIPRIS.

    python tools/sync_publications.py

1. Google Scholar profile  -> the list of papers, patents, citations, h-index
2. OpenAlex (by title)     -> DOI, full author list, author order, corresponding flags
3. KIPRIS Plus (optional)  -> Korean patents (needs KIPRIS_API_KEY env var)
4. tools/publication_overrides.json -> manual fixes

Only the Python standard library is used. If Google Scholar can't be reached
(e.g. a CAPTCHA), the existing publications.js is left untouched.
"""
import datetime
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

# Windows consoles (cp949) can't print every character in paper titles
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets", "js", "publications.js")
CACHE = os.path.join(HERE, "cache", "openalex.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


CFG = load_json(os.path.join(HERE, "sync_config.json"), {})
OVR = load_json(os.path.join(HERE, "publication_overrides.json"), {})


def get(url, headers=None, timeout=30, retries=4):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            raise


def norm_title(s):
    return re.sub(r"[^a-z0-9가-힣]", "", html.unescape(s).lower())


def strip_tags(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"(?<=[A-Za-z]) (\d{1,2}) ?(?=[-‐–)])", lambda m: m.group(1), s)  # "TiO 2 -Supported" -> "TiO2-Supported"


# --------------------------------------------------------------------------
# Lab members (for first / corresponding author badges)
# --------------------------------------------------------------------------
def name_key(name):
    """'Kyeong-Su Kim' -> ('kyeongsu', 'kim'). Assumes Western order (given family)."""
    parts = [re.sub(r"[^a-z]", "", p) for p in re.split(r"[\s\-‐]+", name.lower()) if p]
    parts = [p for p in parts if p]
    if len(parts) < 2:
        return None
    return ("".join(parts[:-1]), parts[-1])


def lab_members():
    names = []
    with open(os.path.join(ROOT, "assets", "js", "data.js"), encoding="utf-8") as f:
        src = f.read()
    names += re.findall(r'\bname:\s*"([^"]+)"', src)
    names += [m if isinstance(m, str) else m.get("name", "") for m in CFG.get("former_members", [])]
    names = [n for n in names if n and "Lab" not in n and "group" not in n.lower()]
    return sorted(set(names))


MEMBERS = lab_members()
MEMBER_KEYS = {}
for n in MEMBERS:
    k = name_key(n)
    if k:
        MEMBER_KEYS[k] = n
        MEMBER_KEYS[(k[1], k[0])] = n  # tolerate "Family Given"
PI_NAME = "Kyeongsu Kim"
PI_ALIASES = {a.lower() for a in CFG.get("pi_aliases", [])}


def match_member(full_name):
    k = name_key(full_name)
    if not k:
        return None
    if k in MEMBER_KEYS:
        return MEMBER_KEYS[k]
    # 'Muhammad Dimas Ramadhan' vs 'Muhammad Ramadhan': same family + same first given name
    first = re.split(r"[\s\-]+", full_name.lower())[0]
    for n in MEMBERS:
        nk = name_key(n)
        if nk and nk[1] == k[1] and re.split(r"[\s\-]+", n.lower())[0] == first and len(first) > 3:
            return n
    return None


COMMON_SURNAMES = {"kim", "lee", "park", "choi", "jung", "jeong", "kang", "cho", "jo", "yoon", "yun", "jang",
                   "lim", "im", "han", "oh", "seo", "shin", "kwon", "hwang", "ahn", "an", "song", "jeon", "hong", "yoo", "ko", "moon"}


def match_initials(n):
    """'SH Choi' -> 'Suk Hoon Choi'. Used only for Scholar's abbreviated author strings.
    A single initial with a common surname ('H Kim') is too ambiguous and is ignored."""
    parts = n.split()
    if len(parts) != 2:
        return None
    ini, fam = parts[0].upper(), parts[1].lower()
    if len(ini) < 2 and fam in COMMON_SURNAMES:
        return None
    for m in MEMBERS:
        mp = re.split(r"[\s\-]+", m)
        if mp[-1].lower() == fam and "".join(w[0].upper() for w in mp[:-1]) == ini:
            return m
    return None


def short_name(full):
    """'Chun-Jae Yoo' -> 'CJ Yoo', 'Hyunjoo J. Lee' -> 'HJ Lee'."""
    parts = [p for p in re.split(r"\s+", full.strip()) if p]
    if len(parts) < 2:
        return full
    fam = parts[-1]
    initials = "".join(ch[0].upper() for p in parts[:-1] for ch in re.split(r"[\-‐.]", p) if ch)
    return f"{initials} {fam}"


# --------------------------------------------------------------------------
# 1. Google Scholar
# --------------------------------------------------------------------------
def fetch_scholar(user):
    items, start = [], 0
    stats = {}
    while True:
        url = f"https://scholar.google.com/citations?user={user}&hl=en&cstart={start}&pagesize=100&sortby=pubdate"
        page = get(url)
        if "gsc_a_tr" not in page and start == 0:
            raise RuntimeError("Google Scholar returned no publications (blocked or CAPTCHA?)")
        if start == 0:
            nums = re.findall(r'class="gsc_rsb_std">(\d+)<', page)
            if len(nums) >= 6:
                stats = {"citations": int(nums[0]), "hindex": int(nums[2]), "i10": int(nums[4])}
        rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.S)
        for r in rows:
            t = re.search(r'class="gsc_a_at">(.*?)</a>', r, re.S)
            link = re.search(r'href="(/citations\?view_op=view_citation[^"]*)"', r)
            grays = [strip_tags(g) for g in re.findall(r'<div class="gs_gray">(.*?)</div>', r, re.S)]
            y = re.search(r'class="gsc_a_h gsc_a_hc gs_ibl">(\d*)<', r)
            c = re.search(r'class="gsc_a_ac gs_ibl">(\d*)<', r)
            items.append({
                "title": strip_tags(t.group(1)) if t else "",
                "scholar": "https://scholar.google.com" + html.unescape(link.group(1)) if link else "",
                "authors": grays[0] if grays else "",
                "venue": grays[1] if len(grays) > 1 else "",
                "year": int(y.group(1)) if y and y.group(1) else None,
                "cites": int(c.group(1)) if c and c.group(1) else 0,
            })
        if len(rows) < 100:
            break
        start += 100
        time.sleep(3)
    return items, stats


def classify(venue, title):
    v = venue.lower()
    if "patent" in v or "특허" in v:
        return "patent"
    if re.search(r"arxiv|chemrxiv|ssrn|biorxiv|preprint|research square", v):
        return "preprint"
    if re.search(r"annual meeting|conference|학술대회|proceedings|symposium|computer aided chemical engineering|meeting", v):
        return "conference"
    if not venue.strip():
        return "preprint"  # listed on Scholar without a venue: submitted / under review
    return "journal"


def clean_venue(venue, kind):
    v = re.sub(r",\s*(19|20)\d\d\s*$", "", venue).strip()
    if kind == "patent":
        return v
    if kind == "conference" and re.match(r"^(19|20)\d\d ", v):
        return v
    # "Chemical Engineering Journal 446, 136578" -> "Chemical Engineering Journal"
    m = re.match(r"^(.*?)(?:\s+\d+\s*(?:\(\d+\))?\s*,.*|\s+\d+\s*$|\s+\d+\s*\(\d+\).*)$", v)
    v = (m.group(1) if m else v).strip(" ,")
    return re.sub(r",\s*(e|[A-Z])?\d{3,}\s*$", "", v).strip(" ,")


# --------------------------------------------------------------------------
# 2. OpenAlex
# --------------------------------------------------------------------------
def _query(title):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", html.unescape(title))).strip()


def _score(key, cand_title, year, cand_year):
    score = difflib.SequenceMatcher(None, key, norm_title(cand_title or "")).ratio()
    if year and cand_year and abs(cand_year - year) > 1:
        score -= 0.1
    return score


OPENALEX_OK = True  # switched off for the rest of the run once the daily quota is hit


def _openalex(params):
    global OPENALEX_OK
    if not OPENALEX_OK:
        return None
    params = {**params, "mailto": CFG.get("contact_email", "")}
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    try:
        return json.loads(get("https://api.openalex.org/works?" + urllib.parse.urlencode(params), retries=2))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("  ! OpenAlex daily quota reached; continuing with Crossref only")
            OPENALEX_OK = False
        return None
    except Exception:  # noqa: BLE001
        return None


def _printed_name(a):
    """Name as printed on the paper. OpenAlex's linked author profile is sometimes the wrong
    person (e.g. 'K W Kim' for Kyeongsu Kim), so the raw byline name wins."""
    raw = (a.get("raw_author_name") or "").strip()
    if "," in raw:  # "Kim, Kyeongsu" -> "Kyeongsu Kim"
        fam, given = [x.strip() for x in raw.split(",", 1)]
        raw = f"{given} {fam}"
    return raw or a["author"].get("display_name") or ""


def _oa_result(w):
    return {
        "doi": w.get("doi"),
        "title": strip_tags(w.get("display_name") or ""),
        "authors": [
            {"name": _printed_name(a),
             "orcid": (a["author"].get("orcid") or "").rsplit("/", 1)[-1],
             "corr": bool(a.get("is_corresponding"))}
            for a in w.get("authorships", [])
        ],
        "src": "openalex", "v": 2,
    }


def lookup(title, year, kind, cache):
    """DOI + full author list (+ corresponding flags when OpenAlex has them).

    Crossref (free, unlimited) finds the DOI; OpenAlex is then asked by DOI,
    which is cheap. A title search on OpenAlex is only the last resort.
    Results are cached in tools/cache/openalex.json, so each paper is looked up once.
    """
    key = norm_title(title)
    hit = cache.get(key)
    if hit and hit.get("src") == "openalex" and hit.get("v") == 2:
        return hit
    result = hit or crossref_lookup(title, year)
    if result and result.get("doi"):
        doi = result["doi"].replace("https://doi.org/", "").lower()
        data = _openalex({"filter": f"doi:{doi}", "per_page": 1})
        if data and data.get("results"):
            result = _oa_result(data["results"][0])
    elif not result:
        data = _openalex({"search": _query(title), "per_page": 8})
        cands = []
        for w in (data or {}).get("results", []):
            sc = _score(key, w.get("display_name"), year, w.get("publication_year"))
            if sc >= 0.88:
                is_pre = w.get("type") in ("preprint", "posted-content") or "ssrn" in (w.get("doi") or "")
                cands.append((kind != "preprint" and is_pre, -sc, w))
        if cands:
            cands.sort(key=lambda c: (c[0], c[1]))
            result = _oa_result(cands[0][2])
    if result:
        cache[key] = result
    time.sleep(0.1)
    return result


def crossref_lookup(title, year):
    """Fallback: Crossref has full author lists (no corresponding-author data)."""
    key = norm_title(title)
    title = re.sub(r"\s*(\.\.\.|…)\s*$", "", title)
    key = norm_title(title)
    params = {"query.bibliographic": _query(title), "rows": 5, "mailto": CFG.get("contact_email", "")}
    try:
        data = json.loads(get("https://api.crossref.org/works?" + urllib.parse.urlencode(params)))
    except Exception as e:  # noqa: BLE001
        print(f"  ! Crossref error for '{title[:50]}': {e}")
        return None
    best, best_sc = None, 0.0
    for w in data.get("message", {}).get("items", []):
        t = (w.get("title") or [""])[0]
        y = (w.get("issued", {}).get("date-parts") or [[None]])[0][0]
        cand = norm_title(t)
        if len(key) > 40 and cand.startswith(key):  # Scholar cut the title short
            cand = cand[:len(key)]
        sc = _score(key, cand, year, y) - (0.05 if w.get("type") == "posted-content" else 0)
        if sc > best_sc:
            best, best_sc = w, sc
    if not best or best_sc < 0.9 or not best.get("author"):
        return None
    return {
        "doi": "https://doi.org/" + best["DOI"],
        "title": strip_tags((best.get("title") or [""])[0]),
        "authors": [{"name": f"{a.get('given', '')} {a.get('family', '')}".strip() or a.get("name", ""), "corr": False}
                    for a in best["author"]],
        "src": "crossref",
    }


# --------------------------------------------------------------------------
# 3. KIPRIS (Korean patents)
# --------------------------------------------------------------------------
def fetch_kipris():
    key = os.environ.get("KIPRIS_API_KEY")
    kc = CFG.get("kipris", {})
    if not key:
        print("  (KIPRIS_API_KEY not set: skipping Korean patents)")
        return []
    base = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"
    out, page = [], 1
    while True:
        q = {"inventors": kc.get("inventor", "김경수"), "applicant": kc.get("applicant", "한국과학기술연구원"),
             "patent": "true", "utility": "true", "numOfRows": 100, "pageNo": page, "ServiceKey": key}
        root = ET.fromstring(get(base + "?" + urllib.parse.urlencode(q)))
        if (root.findtext(".//successYN") or "Y") == "N":
            raise RuntimeError("KIPRIS error: " + (root.findtext(".//resultMsg") or "unknown"))
        items = root.findall(".//item")
        for it in items:
            g = lambda tag: (it.findtext(tag) or "").strip()  # noqa: E731
            reg, opn, app = g("registerNumber"), g("openNumber"), g("applicationNumber")
            date = g("registerDate") or g("openDate") or g("applicationDate")
            if reg:
                label, link = f"KR {reg[:2]}-{reg[2:9]}", f"https://patents.google.com/patent/KR{reg[:9]}B1/ko"
            elif opn:
                label, link = f"KR {opn[:2]}-{opn[2:6]}-{opn[6:13]}", f"https://patents.google.com/patent/KR{opn[2:13]}A/ko"
            else:
                label, link = f"KR {app[:2]}-{app[2:6]}-{app[6:13]} (출원)", ""
            out.append({
                "type": "patent", "country": "KR",
                "t": g("inventionTitle"),
                "j": label,
                "status": g("registerStatus"),
                "y": int(date[:4]) if date[:4].isdigit() else None,
                "u": link,
                "a": [{"n": n.strip()} for n in re.split(r"[,|]", g("applicantName")) if n.strip()],
                "cites": 0,
            })
        total = int(root.findtext(".//totalCount") or 0)
        if page * 100 >= total or not items:
            break
        page += 1
    print(f"  KIPRIS: {len(out)} Korean patents")
    return out


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------
def build():
    user = CFG.get("scholar_user")
    print("Google Scholar ...")
    scholar, stats = fetch_scholar(user)
    print(f"  {len(scholar)} items, {stats}")

    # de-duplicate by title (Scholar sometimes lists a preprint and the paper)
    seen = {}
    for it in scholar:
        k = norm_title(it["title"])
        if k in seen:
            keep = seen[k]
            keep["cites"] = max(keep["cites"], it["cites"])
            if not keep["venue"] and it["venue"]:
                seen[k] = {**it, "cites": keep["cites"]}
        else:
            seen[k] = it
    scholar = list(seen.values())

    cache = load_json(CACHE, {})
    print("OpenAlex ...")
    pubs = []
    for it in scholar:
        kind = classify(it["venue"], it["title"])
        entry = {
            "type": kind,
            "t": it["title"],
            "j": clean_venue(it["venue"], kind),
            "y": it["year"],
            "cites": it["cites"],
            "u": it["scholar"],
        }
        oa = lookup(it["title"], it["year"], kind, cache) if kind != "patent" else None
        if oa and re.search(r"(\.\.\.|…)\s*$", entry["t"]) and oa.get("title"):
            entry["t"] = oa["title"]
        if oa and oa["authors"]:
            if oa.get("doi"):
                entry["u"] = oa["doi"]
            entry["a"] = []
            for a in oa["authors"]:
                member = PI_NAME if a.get("orcid") and a["orcid"] == CFG.get("pi_orcid") else match_member(a["name"])
                au = {"n": short_name(a["name"])}
                if member:
                    au["lab"] = member
                if a["corr"]:
                    au["c"] = 1
                entry["a"].append(au)
        else:
            # fall back to Scholar's (possibly truncated) author string
            names = [n.strip() for n in it["authors"].split(",") if n.strip()]
            entry["a"] = []
            for n in names:
                au = {"n": n}
                if n.lower() in PI_ALIASES:
                    au["lab"] = PI_NAME
                elif match_initials(n):
                    au["lab"] = match_initials(n)
                entry["a"].append(au)
            if it["authors"].rstrip().endswith("..."):
                entry["trunc"] = 1
        if kind == "patent":
            entry["country"] = "US" if entry["j"].upper().startswith("US") else ""
        pubs.append(entry)

    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0)

    print("Patents ...")
    pubs = merge_patents(pubs)

    apply_overrides(pubs)
    drop = set(CFG.get("exclude_types", []))  # e.g. conference abstracts
    pubs = [p for p in pubs if not p.get("_hide") and p["type"] not in drop]
    for p in pubs:
        tag_roles(p)
        tag_topics(p)
    pubs.sort(key=lambda p: (-(p["y"] or 0), -p.get("cites", 0)))
    return pubs, stats


def has(title, fragment):
    """Case- and punctuation-insensitive 'fragment in title'."""
    f = norm_title(fragment)
    return bool(f) and f in norm_title(title)


def merge_patents(pubs):
    """tools/patents.json is the master patent list (one entry per invention, all countries).
    Scholar's copies of the same patents and KIPRIS hits with the same title are folded into it."""
    master = load_json(os.path.join(HERE, "patents.json"), {}).get("patents", [])
    fams = []
    for m in master:
        years = [int(f["d"][:4]) for f in m.get("filings", []) if f.get("d", "")[:4].isdigit()]
        fams.append({"type": "patent", "t": m["t"], "inv": m.get("inv", ""), "filings": m.get("filings", []),
                     "y": max(years) if years else None, "a": [], "cites": 0, "_scholar": m.get("scholar", "")})
    out = []
    for p in pubs:
        if p["type"] == "patent":
            fam = next((f for f in fams if f["_scholar"] and has(p["t"], f["_scholar"])), None)
            if fam:
                fam["en"] = re.sub(r"\s*(\.\.\.|…)\s*$", "", p["t"])
                if p.get("u") and not fam.get("u"):
                    fam["u"] = p["u"]
                continue
        out.append(p)
    try:
        for k in fetch_kipris():
            fam = next((f for f in fams if norm_title(f["t"]) == norm_title(k["t"])), None)
            if fam:
                kr = next((f for f in fam["filings"] if f["c"] == "KR"), None)
                if kr is not None and not kr.get("no"):
                    kr["no"] = k["j"]
                if k.get("u") and not fam.get("u"):
                    fam["u"] = k["u"]
            else:
                out.append(k)
    except Exception as e:  # noqa: BLE001
        print(f"  ! KIPRIS failed: {e}")
    for f in fams:
        f.pop("_scholar", None)
    print(f"  {len(fams)} patents from tools/patents.json")
    return out + fams


def apply_overrides(pubs):
    hide = OVR.get("hide", [])
    roles = load_json(os.path.join(HERE, "pi_roles.json"), {})
    for p in pubs:
        t = p["t"]
        if any(has(t, h) for h in hide):
            p["_hide"] = True
        for rule in OVR.get("type", []):
            if has(t, rule.get("match", "")):
                p["type"] = rule["type"]
        for rule in OVR.get("not_lab", []):
            if has(t, rule.get("match", "")):
                drop = {name_key(n) for n in rule.get("members", [])}
                for a in p["a"]:
                    if a.get("lab") and name_key(a["lab"]) in drop:
                        del a["lab"]
        for rule in OVR.get("first", []):
            if has(t, rule.get("match", "")):
                wanted = {name_key(n) for n in rule.get("authors", [])}
                for a in p["a"]:
                    if a.get("lab") and name_key(a["lab"]) in wanted:
                        a["f"] = 1
        for rule in OVR.get("corresponding", []):
            if has(t, rule.get("match", "")):
                wanted = {name_key(n) for n in rule.get("authors", [])}
                for a in p["a"]:
                    if a.get("lab") and name_key(a["lab"]) in wanted:
                        a["c"] = 1
        # members who are main (first) authors on every paper they appear in
        mains = {name_key(n) for n in CFG.get("main_author_members", [])}
        for a in p["a"]:
            if a.get("lab") and name_key(a["lab"]) in mains:
                a["f"] = 1
        # the PI's own record of each paper beats public metadata
        pi = next((a for a in p["a"] if a.get("lab") == PI_NAME), None)
        if pi is not None and p["type"] != "patent":
            if any(has(t, x) for x in roles.get("corresponding", [])):
                pi["c"] = 1
            if any(has(t, x) for x in roles.get("first", [])):
                pi["f"] = 1
            if any(has(t, x) for x in roles.get("coauthor", [])):
                pi.pop("c", None)
    for x in OVR.get("extra", []):
        pubs.append({"cites": 0, "a": [], **x})


# Research-area tags (same ids as the research page). Keyword rules on the title;
# fix any miss with "topics" in publication_overrides.json.
TOPIC_RULES = {
    "co2": r"co2|co₂|carbon dioxide|carbon capture|capture|formic acid|formate|methanol|electroreduction|electrolys|"
           r"amine|direct air|hydrogen carrier|green-ol|ccs|ccu|이산화탄소|포름산|메탄올|전기분해|전기화학|탄소",
    "biomass": r"biomass|lignin|bio-oil|pyrolysis oil|bio-crude|aviation fuel|jet fuel|jp-10|vanillin|guaiacol|"
               r"lignocellul|biodiesel|organosolv|quercus|xylose|methylfuran|cellulose|isophorone|phenolic|"
               r"바이오|리그닌|항공유|페놀|수첨탈산소",
    "plastic": r"plastic|polyethylene|terephthalate|bhet|pet|pvc|polyvinyl|hydrogenolysis|poly\[|"
               r"플라스틱|폴리에틸렌|pet|탈염소",
    "dft": r"dft|density functional|first-principles|ab initio|mechanistic study",
    "ml": r"machine learning|learning|neural|bayesian|data-driven|narx|markov|unsupervised|reinforcement|"
          r"surrogate|granger|principal component|interpretable|탐색시스템",
    "process": r"process design|process simulation|techno-economic|life cycle|economic|risk|optimization|predictive control|"
               r"rankine|pipeline|distillation|infrastructure|refueling|monitoring|shortcut|thermal management|unit process|recovery of|"
               r"증류|흡수탑|공정",
}


def member_areas():
    """{English name: [areas]} and {Korean name: English name} from data.js.
    Each member sits on one line: { name: "...", areas: [...], ko: "...", ... }"""
    with open(os.path.join(ROOT, "assets", "js", "data.js"), encoding="utf-8") as f:
        src = f.read()
    areas, ko = {}, {}
    for line in src.splitlines():
        m = re.search(r'name:\s*"([^"]+)",\s*areas:\s*\[([^\]]*)\]', line)
        if not m:
            continue
        areas[m.group(1)] = re.findall(r'"(\w+)"', m.group(2))
        k = re.search(r'\bko:\s*"([^"]+)"', line)
        if k:
            ko[k.group(1)] = m.group(1)
    return areas, ko


MEMBER_AREAS, KO_TO_MEMBER = member_areas()


def tag_topics(p):
    text = (p["t"] + " " + p.get("en", "")).lower()
    tags = [k for k, rx in TOPIC_RULES.items() if re.search(rx, text)]
    # author scan: every paper/patent a member worked on is filed under that member's areas
    # (the PI is on everything, so only the other members count)
    authors = {a["lab"] for a in p.get("a", []) if a.get("lab") and a["lab"] != PI_NAME}
    authors |= {KO_TO_MEMBER[n.strip()] for n in p.get("inv", "").split(",") if n.strip() in KO_TO_MEMBER}
    for member in sorted(authors):
        tags += [t for t in MEMBER_AREAS.get(member, []) if t not in tags]
    for rule in OVR.get("topics", []):
        if has(p["t"], rule.get("match", "")):
            tags = rule.get("topics", tags)
    if tags:
        p["topics"] = tags


def tag_roles(p):
    """roles.first = lab members who are (co-)first authors; roles.corr = lab corresponding authors."""
    roles = {}
    if p["type"] != "patent" and p["a"]:
        first = [a["lab"] for i, a in enumerate(p["a"]) if a.get("lab") and (i == 0 or a.get("f"))]
        if first:
            roles["first"] = first
        corr = [a["lab"] for a in p["a"] if a.get("c") and a.get("lab")]
        if corr:
            roles["corr"] = corr
    if roles:
        p["roles"] = roles


def report_new(pubs):
    """List items that were not in the previous publications.js, with their guessed research areas,
    so the areas can be confirmed (and fixed in publication_overrides.json -> topics)."""
    try:
        with open(OUT, encoding="utf-8") as f:
            # one JSON object per line inside window.PUBLICATIONS = [ ... ]
            old = {norm_title(json.loads(line.strip().rstrip(","))["t"])
                   for line in f if line.startswith("  {")}
    except FileNotFoundError:
        return []
    new = [p for p in pubs if norm_title(p["t"]) not in old]
    path = os.path.join(HERE, "cache", "new_items.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([{"t": p["t"], "type": p["type"], "y": p["y"], "topics": p.get("topics", [])} for p in new],
                  f, ensure_ascii=False, indent=1)
    if new:
        print(f"\n{len(new)} NEW item(s). Please confirm the research area of each:")
        for p in new:
            print(f"  - [{', '.join(p.get('topics', [])) or 'no area'}] ({p['type']}, {p['y']}) {p['t'][:90]}")
        print("  Fix areas in tools/publication_overrides.json -> \"topics\".")
    return new


def write(pubs, stats):
    meta = {
        "updated": datetime.date.today().isoformat(),
        "scholar": {"url": f"https://scholar.google.com/citations?user={CFG.get('scholar_user')}"},
    }
    body = (
        "/* Generated by tools/sync_publications.py. Do not edit by hand:\n"
        "   use tools/publication_overrides.json for corrections. */\n"
        f"window.PUBS_META = {json.dumps(meta, ensure_ascii=False)};\n"
        "window.PUBLICATIONS = [\n"
        + ",\n".join("  " + json.dumps({k: v for k, v in p.items() if k != "cites"}, ensure_ascii=False) for p in pubs)
        + "\n];\n"
    )
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(body)
    kinds = {}
    for p in pubs:
        kinds[p["type"]] = kinds.get(p["type"], 0) + 1
    print(f"Wrote {len(pubs)} items to {os.path.relpath(OUT, ROOT)}: {kinds}")
    led = sum(1 for p in pubs if p.get("roles"))
    print(f"  {led} with a lab first/corresponding author detected")


if __name__ == "__main__":
    try:
        pubs, stats = build()
    except Exception as e:  # noqa: BLE001
        print(f"Sync failed, keeping the existing file: {e}")
        sys.exit(1)
    report_new(pubs)
    write(pubs, stats)
