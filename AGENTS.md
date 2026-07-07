<!-- forms-sdk: workspace AGENTS.md schema v3 -->
# Working in this FORMS workspace

This folder is a **FORMS SDK mission workspace**. Everything in it is yours to
edit. `forms` itself is an **installed Python dependency** (like `numpy`) — it
lives in your environment, *not* in this folder, and must not be modified.

## Rules for AI agents

- **Edit only files in this workspace** — `routines/`, `outputs/`, notebooks, and
  scripts you add here. Never edit the installed `forms` package (anything under
  `site-packages/forms/`), and do not clone or vendor its source to change it.
- **Use the `forms` API; do not change the library.** If FORMS does not do what
  you want, the fix is almost always a call you have not made yet — not a source
  edit. `import forms`, then drive everything through the handle: `f = forms.FORMS()`.
- **Keep mission scripts and routines separate — this is the important one.**
  - A **mission** is a full, runnable simulation: configure `forms`, set the
    scenario, propagate it, report the result. Mission scripts live in
    **`missions/`** — one file per scenario, with a descriptive name
    (`missions/leo_formation.py`, not `sim1.py`). `missions/example_mission.py`
    is a worked template; copy and rename it.
  - A **routine** is a small, *reusable calculation* built on `forms`: a function
    of the handle (and forms bricks or your own models) that returns a value, so
    missions can share it. Routines live in **`routines/`**;
    `routines/sdk_routine.py` is the worked example.
  - **Do not put a whole mission script in `routines/`.** If you are writing a
    `def main()` that configures and propagates, it's a mission → `missions/`.

## Learn the API before you build — two doc surfaces

FORMS ships its own documentation inside the package (offline, no setup). Use
**both** surfaces before writing mission code — do not guess an API:

```python
import forms
f = forms.FORMS()

# The CATALOG -- the generated API map: what exists and exactly how to call it
# (symbols, signatures, I/O). Start here to find/verify the call.
f.api_search("sun synchronous")   # matching symbols + signatures, built on demand
f.api_search("eclipse duration")

# The BOOK -- the authored manual: concepts, models, conventions, the *why*.
f.book_search("sun synchronous")  # find pages by topic -> doc_ids
f.book_ai("sun_sync")             # the machine-readable "For AI" subset of a page
```

The loop for any task: **`api_search`** to find/verify the exact symbol and its
I/O → **`book_ai`** the linked page for the model and conventions → write it
against the `forms` handle. (See the Book page `forms.grounding`.)

## Mission conventions

- **Prefer an existing FORMS brick over reinventing.** Physics, orbit design,
  frames, eclipse, geomagnetic field — search `api_search` first; do not re-derive
  what the library already provides.
- **Use matplotlib for plots.** It ships with the SDK. Never hand-roll image/PNG
  encoding, and don't hand-roll CSV/JSON writing where the stdlib does it.
- **Structure a mission** as CONFIGURATION → build → run → report;
  `missions/example_mission.py` is the template.
- **Routines are pure functions of `forms`** (or forms bricks) — no rendering or
  I/O grab-bags. One mission per file; write outputs to `outputs/`.

## Getting started

Open `sdk_quickstart.ipynb` and run it top to bottom — it builds an orbit, records
variables, runs a routine, and finds eclipse windows: the whole SDK in one pass.
To update the library, re-run the pip install from the FORMS README.
