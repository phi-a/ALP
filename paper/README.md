# The manuscript

`main.tex` is written from `Notebook/03-sensitivity/result.md` and the
four derivation notes `Notebook/01-physics/block-{a,b,c,d}-*.md`. A
number in the paper resolves to a check in `tests/`; a claim resolves to
a paragraph in those notes. Change the note first, then the paper.

Prose follows the Closed Form discipline: state the obligation, do the
work, close without new scope.

Project vocabulary and mission framing are recorded in
`Notebook/paper-writing.md`. Check that note before revising manuscript prose.

## Build

```powershell
.\paper\build.ps1
```

or, from `paper/`: `pdflatex main`, `bibtex main`, `pdflatex main` twice.
Build products are git-ignored.

## Bibliography

`references.bib` holds the keys the paper uses;
`alp_dark_matter_30_new_references.bib` the wider ALP literature. Keys
map to `Notebook/references.md`.
