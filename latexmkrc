# latexmk configuration for compiling from the repository root (Overleaf reads only this root file).
# The wrapper journals/working-paper/main.tex uses paths relative to its own folder; from the root, the
# figure and table folders and the bibliography are found through the search paths below. See main.tex.
$pdf_mode = 1;
ensure_path('TEXINPUTS', './manuscript/figures//', './outputs/figures//');
ensure_path('BIBINPUTS', './manuscript/');
$bibtex_use = 2;          # run bibtex when needed; delete .bbl on clean
