"""Differences in the note's results between two versions of the repository (copied from Immo_S2).

Compares the generated tables (outputs/tables/*.csv) at two git revisions. For each table that changed,
it writes the table as it is in the new version with every changed cell shown as "old → new" (rows
matched by their first cell, columns by their header); rows only in the old version are listed after it.
New, removed and unchanged tables are listed at the end. The output is Markdown, for
manuscript/changes.md; each changed table sits in a collapsible block.

Run from the repository root:
    python3 tools/results_diff.py OLD_REV NEW_REV > /tmp/diff.md
"""
import csv
import io
import subprocess
import sys

TABLES = "outputs/tables/"


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def tables(rev):
    """{table name: rows} of the CSV tables at a revision."""
    names = [n for n in git("ls-tree", "--name-only", rev, TABLES).split() if n.endswith(".csv")]
    return {n[len(TABLES):-4]: list(csv.reader(io.StringIO(git("show", f"{rev}:{n}")))) for n in names}


def keys(header):
    """(name, rank among the columns of that name): tables repeat headers such as 'p' or '90% interval'."""
    seen = {}
    out = []
    for h in header:
        seen[h] = seen.get(h, 0) + 1
        out.append((h, seen[h]))
    return out


def changed_table(old, new):
    """(Markdown rows of the new table, changed cells as 'old → new', and the rows dropped from the old;
    number of changed cells)."""
    head, old_head = new[0], old[0]
    col = {key: k for k, key in enumerate(keys(old_head))}            # columns matched by header
    new_keys = keys(head)
    old_rows = {r[0]: r for r in old[1:] if r}
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    n = 0
    for r in new[1:]:
        o = old_rows.get(r[0])
        cells = []
        for k, v in enumerate(r):
            j = col.get(new_keys[k])
            before = o[j] if o is not None and j is not None and j < len(o) else None
            if before is not None and before != v:
                n += 1
                v = f"{before} → {v}"
            cells.append(v)
        out.append("| " + " | ".join(cells) + (" (new row)" if o is None else "") + " |")
    gone = [r for key, r in old_rows.items() if key not in {r[0] for r in new[1:]}]
    if gone:
        out.append("")
        out.append("Rows no longer in the table: " + "; ".join(", ".join(r) for r in gone) + ".")
    if [h for h in old_head if h not in head]:
        out.append("")
        out.append("Columns no longer in the table: " + ", ".join(h for h in old_head if h not in head) + ".")
    return out, n


def main(old_rev, new_rev):
    old, new = tables(old_rev), tables(new_rev)
    lines = [f"Tables compared: `{old_rev}` → `{new_rev}` "
             f"(`python3 tools/results_diff.py {old_rev} {new_rev}`).", ""]
    same = []
    for name in sorted(new):
        if name not in old:
            continue
        if old[name] == new[name]:
            same.append(name)
            continue
        rows, n = changed_table(old[name], new[name])
        lines += [f"<details><summary><code>{name}</code>: {n} cells changed</summary>", ""]
        lines += rows
        lines += ["", "</details>", ""]
    added = [n for n in sorted(new) if n not in old]
    removed = [n for n in sorted(old) if n not in new]
    lines.append("New tables: " + (", ".join(f"`{n}`" for n in added) or "none") + ". Removed: "
                 + (", ".join(f"`{n}`" for n in removed) or "none") + ". Unchanged: "
                 + (", ".join(f"`{n}`" for n in same) or "none") + ".")
    print("\n".join(lines))


if __name__ == "__main__":
    main(*sys.argv[1:3])
