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
- **Routines only.** A **routine** is a small, *reusable calculation* built on
  `forms`: a function of the handle (and forms bricks or your own models) that
  returns a value. Routines live in **`routines/`**; `routines/sdk_routine.py`
  is the worked example.
- **This workspace has no `missions/` folder.** The project's own simulation
  lives in `src/darknessalp/` and `jupyter/darkness_alp_sim.ipynb` and does not
  use FORMS. FORMS is kept here only as an independent cross-check of that
  simulation — see `Notebook/02-mission-analysis/testing.md`.

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
- **Routines are pure functions of `forms`** (or forms bricks) — no rendering or
  I/O grab-bags. Write outputs to `outputs/`.

## Getting started

Use `f.api_search` and `f.book_ai` as above to find the call you need, then write
a routine in `routines/`. To update the library, re-run the pip install from the
FORMS README.
