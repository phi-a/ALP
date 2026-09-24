# CLAUDE.md — darknessALP

## Purpose
Teaching codebase. The student audience is the primary constraint on every decision.

## Language
- Python 3.10+ with `numpy`, `scipy`, `astropy`, `matplotlib`. Use them:
  astropy owns time and frames, scipy owns integration and rotations,
  numpy owns arrays. The student calls `propagate`, never sees RK45.
- Custom models only where no package does the job (IGRF, the line-of-
  sight integral, cutoff rigidity, backgrounds, FOV geometry).
- Keep the package count at those four; anything new goes into
  `requirements.txt` with a reason. No FORMS in the student path.
- As little code as possible: functions on arrays, vectorised over rows,
  no classes.

## Style — strict PEP 8
- 79-char line limit.
- `snake_case` for everything (variables, functions, files). `UPPER_SNAKE` for module-level constants only.
- One blank line between logical blocks inside a function; two between top-level definitions.
- Run mentally through PEP 8 before proposing any code.

## File / module layout
- `src/darknessalp/<topic>/` subpackages, one topic per file, a few
  short functions each. Topics: `frames` (astropy time and reference
  frames), `orbit` (CCSDS elements, `propagate` point or J2, OEM),
  `dynamics` (accelerations and torques, no integration), `kinematics` (body
  attitude, slews, rate-limited steering), `pointing` (target specs,
  modes = target + roll rule, condition → mode schedules, constraints),
  `field` (IGRF, dipole, magnetic coordinates), `geometry` (LOS
  integral, limb, umbra, FOV), `background` (CXB, GRXE, NXB proxy,
  sources), `source` (halo column density, ALP source spectra), `sim`
  (state table).
- Each `__init__.py` re-exports its topic's public API; nothing else.
- Functions take and return numpy arrays shaped `(N, 3)` or `(N,)`;
  positions in km, fields in tesla, angles in degrees, time as astropy
  `Time`.
- Run scripts live outside `src/`: `scripts/` for thin argparse tools,
  `jupyter/` for the simulation run notebooks that build a sequence and
  show results. Nothing in `src/` prints or plots.
- Tests mirror the topics: `tests/test_<topic>.py`, plus
  `test_invariants`, `test_validation_gates` (published numbers) and
  `test_scenario_regression` (pinned end-to-end answers). Run them with
  `python -m pytest`, never `unittest discover`.
- A new public function needs a docstring and a known-answer test, and
  the API reference regenerated.

## Where things go
- `jupyter/main_sequence.ipynb` is the one simulation pipeline, a living
  document kept current. A variant that tests something different is a
  copy named `main_sequence_vN.ipynb` (N = 1, 2, …) whose first cell says
  what it tests; its result goes in a dated `Notebook/` note.
- `jupyter/conops.ipynb` is the picture book: figures for intuition
  and ConOps graphics, drawn from the same simulated mission; the
  figure code lives in `scripts/conops_figures.py`. Other `jupyter/`
  notebooks are analyses that run on the same library.
  `Notebook/` notes (.md, tracked). `docs/` references (untracked).
  `data/` inputs. `outputs/` generated (untracked).
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
- Classes. Functions on arrays; a dict of arrays is the record type.
- Hand-rolled numerics that scipy or astropy already provide.
- Abstract base classes, decorators, metaclasses — not in this repo.
- Type annotations are optional; add them only if they clarify, not clutter.
