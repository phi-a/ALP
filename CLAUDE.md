# CLAUDE.md — darknessALP

## Purpose
Teaching codebase. The student audience is the primary constraint on every decision.

## Language
- Python 3.10+. Standard library first for the student-path scripts in
  `src/darknessalp/`; the trig and the integrals are the teaching content.
- `numpy`, `scipy`, `astropy`, `matplotlib` are allowed where they
  genuinely simplify (analysis layer, plots, test oracles). Keep the
  package count low; anything new goes into `requirements.txt`.
- No FORMS in the student path. It is the mentor's cross-check, later.

## Style — strict PEP 8
- 79-char line limit.
- `snake_case` for everything (variables, functions, files). `UPPER_SNAKE` for module-level constants only.
- One blank line between logical blocks inside a function; two between top-level definitions.
- Run mentally through PEP 8 before proposing any code.

## File / module layout
- One function per file where practical. Files live in `src/darknessalp/`.
- File name = function name (e.g. `compute_orbit.py` contains `compute_orbit()`).
- `__init__.py` re-exports the public API; nothing else.
- Tests mirror the source: `tests/test_compute_orbit.py` tests `compute_orbit()`.
- `src/darknessalp/bfield/` and `yamamoto/` are legacy (numpy, old naming);
  convert to the rules above one file at a time, don't extend them.

## Where things go
- `jupyter/` notebooks. `Notebook/` notes (.md, tracked). `docs/` references
  (untracked). `data/` inputs. `freeflyer/` FreeFlyer scripts. `outputs/`
  generated (untracked).
- New decisions and results summaries go in `Notebook/`, dated.

## Code length
- Minimise character count. No padding, no boilerplate prose.
- Docstrings: one short line — what it returns, not how it works.
- Comments: one brief phrase; never a sentence that restates the code.
- No blank placeholder comments, no TODO blocks, no verbose error messages.

## I/O and arguments
- Scripts that run standalone use `argparse` — brief `help=` strings only.
- Print output only when the user asked for output. No debug prints left in.
- File paths come in as arguments; never hardcoded.

## What to avoid
- Clever one-liners that sacrifice readability. Students read this.
- Deep nesting. Flatten with early returns.
- Classes unless state genuinely needs to travel. Functions first.
- Abstract base classes, decorators, metaclasses — not in this repo.
- Type annotations are optional; add them only if they clarify, not clutter.
