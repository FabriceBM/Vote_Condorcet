# Reference checks

Has the bibliography of the note (`../../manuscript/references.bib`, 98 entries) been verified, and how?

| File | Check |
|---|---|
| `2026-10-21_web-search.md` | First check, by two agents through web search: publisher pages, RePEc, JSTOR listings, repositories. The official databases (Crossref, doi.org) were blocked at the time, so fields that could not be confirmed were flagged with `verify` |
| `2026-10-22_official-records.md`, `.csv` | Second check, against the official records. Written by `../../tools/check_references.py`: each entry is compared with its Crossref record (by DOI, or found by search), and with arXiv or the document's own page for preprints and web documents, on title, authors, year, journal, volume, issue and pages. Every DOI is also tested at doi.org |

## Result of the second check (22 Oct. 2026)

**No entry is fabricated.** Every one of the 98 works was found in an official record, or for the few the
databases do not cover, in an independent index or through papers that cite it.

| Status | Entries | Meaning |
|---|---|---|
| match | 66 | Every compared field agrees with the official record, and the DOI resolves |
| minor | 19 | Formatting only: Crossref stores only the first page of old JSTOR articles; issue `1-2` against `1–2`; a book series named instead of the book title; a URL appended to a title in the record |
| explained | 13 | See the table below |

### The 13 entries the script could not match automatically

| Entry | Why | Verified by |
|---|---|---|
| Condorcet (1785) | The only Crossref record is the Cambridge University Press reissue (2014) | The reissue (doi 10.1017/cbo9781139923972) reproduces the 1785 Essai |
| Arrow (1951) | The only Crossref record is the Yale re-edition (2012/2017) | Reviews of the 1951 edition (e.g. Baumol, *Econometrica* 1952) |
| Buchanan & Tullock (1962) | The search returned a 1964 review of the book | The book's University of Michigan Press record (doi 10.3998/mpub.7687, which gives 1960) and reviews of 1963–64 |
| Regenwetter et al. (2006) | The book has no Crossref record. The DOI that the first check had suggested (and flagged, never used) belongs to another book | Reviews in *Social Choice and Welfare* 31(2), 2008, and *Choice* 44-3496, 2007 |
| Tideman (2006) | The Ashgate edition has no Crossref record | Routledge reissue (doi 10.4324/9781315259963); three reviews in *Public Choice* 133, 2007 |
| Moulin (1983) | The book itself has no Crossref record | Its chapters' records (Elsevier, ISBN 978-0-444-86371-3) |
| Balinski & Laraki (2011) | Crossref stores the title without its subtitle | DOI 10.7551/mitpress/9780262015134.001.0001, MIT Press, 2011 |
| Tsebelis (2002) | Crossref stores the title without its subtitle | DOI 10.1515/9781400831456, Princeton University Press, 2002 |
| Brandt et al. (2016), handbook | Crossref lists the author of the foreword (Moulin) rather than the editors | DOI 10.1017/CBO9781107446984; title and year agree |
| Plott (1967) | No Crossref record (*American Economic Review*, 1967) | The paper in the Consensus index, and McKelvey et al. (1976) citing it as *Amer. Econom. Rev.* 57: 787–806 |
| Felsenthal & Machover (2008) | No Crossref record (*Homo Oeconomicus*) | The paper in the Consensus index (Felsenthal & Machover, 2008) |
| Kemeny (1959) | No Crossref record (*Daedalus*, 1959) | Reference lists deposited in Crossref by Young & Levenglick (1978), Young (1988), Bartholdi et al. (1989): *Daedalus* 88: 571–591. Kondratev & Nesterov (2020) give 577. The entry now uses 571–591 and stays flagged until JSTOR settles it |
| EU Treaty, art. 16 | EUR-Lex refuses automated requests (HTTP 202) | The article text was checked on 21 Oct. through the Council of the EU and legislation.gov.uk; only the Official Journal page numbers remain unconfirmed |

## Corrections made after the second check

- **DOIs added**, each confirmed against its record and tested at doi.org:
  - Satterthwaite (1975), Nakamura (1979), Greenberg (1979), Rae (1969), Gehrlein & Fishburn (1976);
  - Simpson (1969), Fishburn (1984), Laffond, Laslier & Le Breton (1993), Bartholdi et al. (1989, manipulation);
  - Faliszewski & Procaccia (2010), Brandt, Geist & Peters (2017), Guilbaud (1952), Kondratev & Ianovski (2024);
  - Casella (2005), Tsebelis (2002), Balinski & Laraki (2011).
- **Guilbaud (1952).** The Persée record confirms *Économie appliquée* 5(4): 501–584. The alternative range
  501–551 is wrong.
- **Balinski & Laraki.** The year is 2011, as in the MIT Press record; the first check had set 2010 from the
  copyright page.
- **Issue numbers aligned on the records:**
  - Holliday & Pacuit (2023), 197(1–2);
  - Glynia et al. (2026), 208(3–4);
  - Kondratev & Nesterov (2020), 183(1–2), with the second author's first name, Alexander;
  - Krick (2017), issue 1.
- **Kemeny (1959).** Pages 571–591, from the three earliest citing papers.
- **Flags removed:** 24 `verify` fields are now confirmed by the records.

**Still flagged, 3 entries** (`grep -n verify ../../manuscript/references.bib`):
- Kemeny (1959): the first page;
- Regenwetter et al. (2006): no DOI known;
- the EU Treaty: the Official Journal page numbers.

## What these checks do not cover

They verify that each reference exists and is described correctly. They do not verify that each paper says what
the note attributes to it: that rests on the abstracts and on the first check's reading. The key ideas in
`../concept-map/references.csv` are stated at that level.

## Rerun

```bash
python3 tools/check_references.py     # needs api.crossref.org, doi.org, export.arxiv.org and the document sites
```
