"""Check every entry of manuscript/references.bib against its official record.

For each entry:
    with a DOI       the Crossref record of that DOI (https://api.crossref.org/works/<doi>), and the DOI must
                     resolve at doi.org;
    without a DOI    a Crossref bibliographic search (title, first author), then OpenAlex if Crossref finds
                     nothing close; a match proposes a DOI;
    arXiv preprints  the arXiv record (export.arxiv.org);
    web documents    the page itself must contain the title (RFC, Debian constitution, EU Treaty).
Compared fields: title, authors (surnames, in order), year, journal or book title, volume, issue, pages.

Writes literature/reference-checks/<date>_official-records.md (one line per entry, then the details of every
difference) and .csv. Needs network access to api.crossref.org, doi.org, api.openalex.org, export.arxiv.org
and the sites of the web documents.

Run from the repository root:
    python3 tools/check_references.py
"""
import csv
import datetime
import difflib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from concept_map import detex, read_bib, split_authors            # noqa: E402

BIB = "manuscript/references.bib"
OUT_DIR = "literature/reference-checks"
UA = "Vote_Condorcet reference check (https://github.com/FabriceBM/Vote_Condorcet)"
WEB = {   # web documents: url, text the page must contain
    "Resnick2014rfc7282": ("https://www.rfc-editor.org/rfc/rfc7282.txt", "On Consensus and Humming in the IETF"),
    "Debian2024constitution": ("https://www.debian.org/devel/constitution", "Constitution for the Debian Project"),
    "TEU2016art16": ("https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:12016M/TXT",
                     "Treaty on European Union"),
}


def get(url, accept="application/json", tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.status, r.read().decode("utf8", "replace"), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, "", url
            if k == tries - 1:
                return e.code, "", url
        except Exception as e:                                      # noqa: BLE001
            if k == tries - 1:
                return 0, str(e), url
        time.sleep(2 * (k + 1))


def norm(s):
    s = unicodedata.normalize("NFKD", detex(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def bib_surnames(e):
    return [norm(last).split()[-1] if norm(last) else "" for last, _ in
            split_authors(e.get("author") or e.get("editor", ""))]


def pages(p):
    p = (p or "").replace("--", "-").replace("–", "-")
    return [x.strip() for x in p.split("-") if x.strip()]


def crossref_fields(m):
    def year(key):
        d = m.get(key, {}).get("date-parts", [[None]])
        return d[0][0] if d and d[0] else None
    return {
        "title": (m.get("title") or [""])[0],
        "surnames": [norm(a.get("family", a.get("name", ""))).split()[-1] if norm(a.get("family", a.get("name", "")))
                     else "" for a in m.get("author", m.get("editor", []))],
        "years": {y for y in (year("issued"), year("published-print"), year("published-online"),
                              year("published")) if y},
        "venue": (m.get("container-title") or [""])[0],
        "volume": m.get("volume", ""), "issue": m.get("issue", ""), "page": m.get("page", ""),
        "doi": m.get("DOI", ""), "type": m.get("type", ""), "publisher": m.get("publisher", ""),
    }


def compare(e, r):
    """Differences between a bib entry and an official record (dict of crossref_fields form)."""
    diffs = []
    t = sim(e.get("title", ""), r["title"])
    if t < 0.93:
        diffs.append(("title", detex(e.get("title", "")), r["title"], "major" if t < 0.7 else "minor"))
    bs, rs = bib_surnames(e), [s for s in r["surnames"] if s]
    if rs and bs:
        if bs != rs[:len(bs)] or len(bs) != len(rs):
            diffs.append(("authors", ", ".join(bs), ", ".join(rs),
                          "major" if not set(bs) & set(rs) else "minor"))
    by = int(re.sub(r"\D", "", e.get("year", "0")) or 0)
    if r["years"] and by not in r["years"]:
        diffs.append(("year", str(by), "/".join(map(str, sorted(r["years"]))), "major"))
    venue = e.get("journal") or e.get("booktitle") or ""
    if venue and r["venue"] and sim(venue, r["venue"]) < 0.85:
        diffs.append(("journal", detex(venue), r["venue"], "minor"))
    for f in ("volume", "issue"):
        bf = detex(e.get(f if f == "volume" else "number", ""))
        if bf and r[f] and norm(bf) != norm(r[f]):
            diffs.append((f, bf, r[f], "major" if f == "volume" else "minor"))
    bp, rp = pages(detex(e.get("pages", ""))), pages(r["page"])
    if bp and rp and bp != rp:
        diffs.append(("pages", "-".join(bp), "-".join(rp), "major" if bp[0] != rp[0] else "minor"))
    return diffs


def check_doi(key, e):
    doi = e["doi"].strip()
    code, body, _ = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if code != 200:
        # not a Crossref DOI (e.g. DataCite): fall back to OpenAlex
        code2, body2, _ = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
        if code2 != 200:
            return "doi not found", [], {"doi": doi}
        return openalex_result(e, json.loads(body2), "OpenAlex (DOI)")
    r = crossref_fields(json.loads(body)["message"])
    rcode, _, final = resolve(doi)
    status = "match" if not (d := compare(e, r)) else ("differs" if any(x[3] == "major" for x in d) else "minor")
    if rcode not in (200, 301, 302, 303, 307, 308, 403):
        d.append(("doi.org", doi, f"HTTP {rcode}", "major"))
        status = "differs"
    return status, d, {**r, "source": "Crossref (DOI)", "resolves": final}


def resolve(doi):
    try:
        req = urllib.request.Request("https://doi.org/" + doi, method="HEAD", headers={"User-Agent": UA})
        opener = urllib.request.build_opener(NoRedirect)
        with opener.open(req, timeout=40) as r:
            return r.status, "", r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, "", e.headers.get("Location", "")
    except Exception:                                               # noqa: BLE001
        return 0, "", ""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def search(key, e):
    title, surnames = detex(e.get("title", "")), bib_surnames(e)
    q = urllib.parse.quote(f"{title} {surnames[0] if surnames else ''}")
    code, body, _ = get(f"https://api.crossref.org/works?query.bibliographic={q}&rows=5")
    best = None
    if code == 200:
        for m in json.loads(body)["message"]["items"]:
            r = crossref_fields(m)
            score = sim(title, r["title"]) + (0.1 if surnames and surnames[0] in r["surnames"][:1] else 0)
            if not best or score > best[0]:
                best = (score, r)
    if best and best[0] >= 1.0:
        r = best[1]
        d = compare(e, r)
        return ("found, DOI to add" if not d else "found, differs"), d, {**r, "source": "Crossref (search)"}
    # OpenAlex
    q = urllib.parse.quote(title)
    code, body, _ = get(f"https://api.openalex.org/works?search={q}&per-page=5")
    if code == 200:
        for w in json.loads(body).get("results", []):
            if sim(title, w.get("title") or "") >= 0.9:
                return openalex_result(e, w, "OpenAlex (search)")
    return "not found", [], {}


def openalex_result(e, w, source):
    r = {"title": w.get("title") or "", "surnames": [norm(a["author"]["display_name"]).split()[-1]
                                                   for a in w.get("authorships", []) if norm(a["author"]["display_name"])],
         "years": {w.get("publication_year")} - {None},
         "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
         "volume": (w.get("biblio") or {}).get("volume") or "", "issue": (w.get("biblio") or {}).get("issue") or "",
         "page": "-".join(x for x in ((w.get("biblio") or {}).get("first_page"),
                                      (w.get("biblio") or {}).get("last_page")) if x),
         "doi": (w.get("doi") or "").replace("https://doi.org/", ""), "type": w.get("type", ""),
         "source": source}
    d = compare(e, r)
    status = "match" if not d else ("differs" if any(x[3] == "major" for x in d) else "minor")
    if source.endswith("(search)"):
        status = "found (OpenAlex)" + ("" if not d else ", differs")
    return status, d, r


def check_arxiv(key, e, arxiv_id):
    code, body, _ = get(f"https://export.arxiv.org/api/query?id_list={arxiv_id}", accept="application/atom+xml")
    m = re.search(r"<entry>.*?<title>(.*?)</title>", body, re.S)
    if code != 200 or not m:
        return "arXiv not found", [], {}
    names = re.findall(r"<name>(.*?)</name>", body)
    r = {"title": " ".join(m.group(1).split()), "surnames": [norm(n).split()[-1] for n in names],
         "years": set(), "venue": "", "volume": "", "issue": "", "page": "", "doi": "", "source": "arXiv"}
    d = compare(e, r)
    return ("match" if not d else "minor" if all(x[3] == "minor" for x in d) else "differs"), d, r


def check_web(key, e):
    url, text = WEB[key]
    code, body, _ = get(url, accept="text/html,text/plain")
    ok = code == 200 and norm(text) in norm(body)
    return ("match" if ok else f"page check failed (HTTP {code})"), [], {"source": url}


def main():
    bib = read_bib(BIB)
    today = datetime.date.today().isoformat()
    rows, details = [], []
    for k, e in bib.items():
        arxiv = re.search(r"arXiv:(\d{4}\.\d{4,5})", e.get("note", "") + " " + e.get("url", ""))
        if k in WEB:
            status, d, r = check_web(k, e)
        elif e.get("doi"):
            status, d, r = check_doi(k, e)
        elif arxiv:
            status, d, r = check_arxiv(k, e, arxiv.group(1))
        else:
            status, d, r = search(k, e)
        rows.append([k, status, r.get("source", ""), r.get("doi", "") if not e.get("doi") else e["doi"],
                     "; ".join(f"{f}: bib '{a}' vs record '{b}' ({sev})" for f, a, b, sev in d)])
        if d or status not in ("match",):
            details.append((k, status, r, d))
        print(f"  {k:<32} {status}")
        time.sleep(0.3)
    os.makedirs(OUT_DIR, exist_ok=True)
    base = os.path.join(OUT_DIR, f"{today}_official-records")
    with open(base + ".csv", "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["key", "status", "source", "doi", "differences"])
        w.writerows(rows)
    counts = {}
    for r in rows:
        counts[r[1]] = counts.get(r[1], 0) + 1
    with open(base + ".md", "w", encoding="utf8") as fh:
        fh.write(f"# Bibliography against official records, {today}\n\n")
        fh.write("Written by `tools/check_references.py`: every entry of `manuscript/references.bib` compared with "
                 "its Crossref record (by DOI, or found by search), OpenAlex, arXiv, or the page of a web document. "
                 "Fields: title, authors, year, journal, volume, issue, pages.\n\n")
        fh.write("| Status | Entries |\n|---|---|\n")
        for s, n in sorted(counts.items(), key=lambda x: -x[1]):
            fh.write(f"| {s} | {n} |\n")
        fh.write("\n## Entries to look at\n\n")
        for k, status, r, d in details:
            fh.write(f"### {k}: {status}\n\n")
            if r.get("source"):
                fh.write(f"Source: {r['source']}" + (f"; DOI {r['doi']}" if r.get("doi") else "") + "\n\n")
            for f, a, b, sev in d:
                fh.write(f"- **{f}** ({sev}): bib `{a}`; record `{b}`\n")
            fh.write("\n")
    print(f"  {base}.md and .csv: " + ", ".join(f"{n} {s}" for s, n in counts.items()))


if __name__ == "__main__":
    main()
