---
type: note
tags: [darkness, alp, admin]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# 2026-09-17 — one project, one place

Merged `Python/darkmatter/ALP` and the Library notes into this repo
(`Python/darknessALP`, GitHub `phi-a/darknessALP`).

## Layout

- `src/darknessalp/` — package. `bfield/` (IGRF13, CHAOS), `yamamoto/`
  (Suzaku + Yamamoto 2020 validation), `fetch_axion_limit.py`,
  `list_axion_limits.py`
- `jupyter/` — all notebooks
- `Notebook/` — this second memory (tracked)
- `docs/` — references (not tracked)
- `data/` — `bfield/`, `axionlimits/` tracked; `suzaku/` not tracked
- `freeflyer/` — FreeFlyer scripts
- `outputs/` — generated, not tracked

## Axion archive

Source: https://github.com/cajohare/AxionLimits (`limit_data/<coupling>/`).
`list_axion_limits(coupling)` lists files; `fetch_axion_limit(name,
coupling)` downloads once into `data/axionlimits/<coupling>/` and returns
`(masses, couplings)`. Not tied to Fig. 7 — use it for any limit or
projection. `jupyter/Yamamoto2020_Fig7.ipynb` reproduces the paper;
the DarkNESS projection can reuse the same loader.

## Later

- `yamamoto/` and `bfield/` still use numpy and old naming; bring to the
  teaching style one file at a time (priority: bfield, then axion plot).
- `jupyter/Yamamoto.ipynb`, `Yamamoto2.ipynb`, `ObsStudy.ipynb` are old
  exploration; keep until the cohort notebooks fully replace them.
- `data/suzaku/` (2.4 GB) was not copied; `suzaku_archive.py` re-downloads
  on demand.
- `06-yamamoto-suzaku-archive/` holds older versions of notes that also
  exist in `04-plan/`; merge or delete. *Deleted 2026-09-19.*
