# Reference checks

Has the bibliography of the note (`../../manuscript/references.bib`, 98 entries) been verified, and how?

| File | Check |
|---|---|
| `2026-10-21_web-search.md` | First check, by two agents through web search: publisher pages, RePEc, JSTOR listings, repositories. The official databases (Crossref, doi.org) were blocked at the time, so fields that could not be confirmed were flagged with `verify` |
| `2026-10-22_official-records.md`, `.csv` | Second check, against the official records. Written by `../../tools/check_references.py`. Each entry is compared, on title, authors, year, journal, volume, issue and pages, with: its Crossref record (by DOI, or found by search), tested at doi.org; for books without a DOI, the Library of Congress catalogue record (by LCCN); for the EU Treaty, the record and the Official Journal of the EU Publications Office (by CELEX number); for two articles in journals without an online record, the record of the author's institutional repository; arXiv or the document's own page for preprints and web documents |

## Result of the second check (22 Oct. 2026)

**97 of the 98 entries are confirmed by their official record. One is not yet, Kemeny (1959): its only
record is on JSTOR, which refuses automated access.** No entry is fabricated: Kemeny (1959) is also found
in the reference lists of other papers.

| Status | Entries | Meaning |
|---|---|---|
| match | 74 | Every compared field agrees with the official record, and the DOI resolves |
| minor | 19 | Formatting only: Crossref stores only the first page of old JSTOR articles; issue `1-2` against `1–2`; a book series named instead of the book title; a URL appended to a title in the record |
| confirmed by hand | 4 | The official record exists and agrees, but the script cannot match it (first table below) |
| not yet confirmed | 1 | No official record reachable (second table below). Marked `verify` in `references.bib` |

### Confirmed by hand

| Entry | Why the script does not match it | Official record |
|---|---|---|
| Moulin (1983) | The book itself has no Crossref record | Its chapters' records (Elsevier, ISBN 978-0-444-86371-3) |
| Balinski & Laraki (2011) | Crossref stores the title without its subtitle | DOI 10.7551/mitpress/9780262015134.001.0001, MIT Press, 2011 |
| Tsebelis (2002) | Crossref stores the title without its subtitle | DOI 10.1515/9781400831456, Princeton University Press, 2002 |
| Brandt et al. (2016), handbook | Crossref lists the author of the foreword (Moulin) rather than the editors | DOI 10.1017/CBO9781107446984; title and year agree |

### Not yet confirmed

| Entry | Why | What other papers say | To settle it |
|---|---|---|---|
| Kemeny (1959) | No Crossref record; JSTOR refuses automated access, and no other record of *Daedalus* 1959 is reachable | *Daedalus* 88, first page 577 in Fishburn (1977) and Kondratev & Nesterov (2020), and in most lists found by the first check; 571 in Young & Levenglick (1978), Young (1988) and Bartholdi et al. (1989). The entry keeps 577–591 | JSTOR [20026529](https://www.jstor.org/stable/20026529), in a browser |

## Corrections made after the second check

- **DOIs added**, each confirmed against its record and tested at doi.org:
  - Satterthwaite (1975), Nakamura (1979), Greenberg (1979), Rae (1969), Gehrlein & Fishburn (1976);
  - Simpson (1969), Fishburn (1984), Laffond, Laslier & Le Breton (1993), Bartholdi et al. (1989, manipulation);
  - Faliszewski & Procaccia (2010), Brandt, Geist & Peters (2017), Guilbaud (1952), Kondratev & Ianovski (2024);
  - Casella (2005), Tsebelis (2002), Balinski & Laraki (2011).
- **Library of Congress control numbers added** to the 5 books without a DOI. Each record agrees on title,
  year, publisher and authors:
  - Condorcet (1785), [06005363](https://www.loc.gov/item/06005363/): Paris, Imprimerie royale;
  - Arrow (1951), [51009755](https://www.loc.gov/item/51009755/): New York, Wiley. The series, Cowles
    Commission Monograph No. 12, is confirmed by the record of a 1951 review (doi 10.1515/jbnst-1951-1630148);
  - Buchanan & Tullock (1962), [62007705](https://www.loc.gov/item/62007705/): Ann Arbor, University of
    Michigan Press;
  - Regenwetter et al. (2006), [2005023291](https://www.loc.gov/item/2005023291/): Cambridge University Press.
    The record names the first author only; the four authors and the ISBN are on the catalogue records it
    shares with Open Library. The book has no DOI: the one suggested by the first check (never used) belongs
    to another book;
  - Tideman (2006), [2006021134](https://www.loc.gov/item/2006021134/): Aldershot, Ashgate. The ISBN as
    above.
- **Two articles confirmed by the institutional repository of their author.** Neither journal has an
  online record for these years: *Homo Oeconomicus*' own site no longer resolves, and JSTOR refuses automated
  access. The repository records agree on every field of the entries:
  - Plott (1967): Caltech Library, [CaltechAUTHORS 20140220-101651369](https://authors.library.caltech.edu/records/rzmbm-kft47):
    *American Economic Review* 57(4): 787–806, September 1967, linked to JSTOR 1815369;
  - Felsenthal & Machover (2008): LSE Research Online, [24213](https://researchonline.lse.ac.uk/id/eprint/24213/):
    *Homo Oeconomicus* 25(3/4): 319–334, 2008. The cover sheet of the accepted manuscript held there gives the
    same citation. Felsenthal (2012) cites the article as 319–333; the entry follows the LSE record. Its URL
    now points to that record, where the manuscript is free to read.
- **The EU Treaty.** The EU Publications Office confirms the CELEX number 12016M/TXT, the English title, and
  publication in the Official Journal C 202 of 7 June 2016. Its PDF of that issue shows Article 16 on page
  C 202/24, with the blocking minority of "at least four Council members" in paragraph 4. The entry now
  cites that page, with the ELI identifier `data.europa.eu/eli/treaty/teu_2016/oj` as its URL.
- **Guilbaud (1952).** The Persée record confirms *Économie appliquée* 5(4): 501–584. The alternative range
  501–551 is wrong.
- **Balinski & Laraki.** The year is 2011, as in the MIT Press record; the first check had set 2010 from the
  copyright page.
- **Issue numbers aligned on the records:**
  - Holliday & Pacuit (2023), 197(1–2);
  - Glynia et al. (2026), 208(3–4);
  - Kondratev & Nesterov (2020), 183(1–2), with the second author's first name, Alexander;
  - Krick (2017), issue 1.
- **Flags:** 27 of the 28 `verify` fields of v0.1 are now confirmed by the records; Kemeny (1959) keeps its
  flag.

## What these checks do not cover

They verify that each reference exists and is described correctly. They do not verify that each paper says what
the note attributes to it: that rests on the abstracts and on the first check's reading. The key ideas in
`../concept-map/references.csv` are stated at that level.

## Rerun

```bash
python3 tools/check_references.py
```

It needs api.crossref.org, doi.org, api.openalex.org, export.arxiv.org, www.loc.gov, publications.europa.eu,
authors.library.caltech.edu, researchonline.lse.ac.uk and the document sites; `pdftotext` (poppler) for the
Official Journal page check.
