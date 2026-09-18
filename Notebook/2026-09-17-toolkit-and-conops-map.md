---
type: note
tags: [darkness, alp, admin, log]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# 2026-09-17 — ConOps map, toolkit, first sky scan

What happened today and where each piece went.

## Done

- **ConOps ↔ physics map** — which ConOps variable touches which physics
  term, the pointing tiers by mission cost, Earth occultation as the free
  "off" state, plasma shown negligible.
  → [[02-mission-analysis/conops-physics-map]]
- **Toolkit, twice.** Morning: 27 stdlib one-function scripts, 51
  tests (D19). Afternoon: rebuilt as a numpy/scipy/astropy library in
  topic subpackages (`frames orbit dynamics kinematics pointing field
  geometry background sim`), 31 tests carrying the same known answers,
  `scripts/fov_view.py`, and the run notebook
  `jupyter/darkness_alp_sim.ipynb` (D21). The vectorised LOS integral
  is 60× faster.
  → [[02-mission-analysis/tooling]]
- **Pointing system** — target specs (inertial, bodies, orbit-based,
  field-based), modes with analytic roll, condition → mode schedules,
  rate-limited steering with quaternions and no dynamics.
  → [[02-mission-analysis/pointing-system]]
- **First full-day run** — GC fixed target, ISS-like, 2027-05-01:
  corr($K$, $R_c$) = +0.74, corr($K$, limb) = −0.87 on 513 usable sky
  frames. → [[02-mission-analysis/tooling]] §First run
- **Testing scheme** — five layers (known answers, invariants,
  cross-checks, published-number gates, regression pins); 58 tests under
  `python -m pytest`. Found four real bugs, including `circular_orbit`
  measuring altitude above the IGRF sphere instead of the WGS84
  equatorial radius. → [[02-mission-analysis/testing]]
- **Cleanup** — jupyter/ reduced to the sim run file, Yamamoto 2020
  Fig 7, and the allowed-signal ceiling; FORMS and old Suzaku notebooks,
  `yamamoto/`, `bfield/` and their tests removed (all in git history).
  Fig 7 now uses `fetch_axion_limit` instead of its own downloader.
  `missions/` removed; `routines/` kept for the FORMS cross-check. The
  two Suzaku validation records are marked archived.
- **Field-integral gates pass** — closed forms, $L_{\max}$ plateau,
  reversal cancellation. → [[02-mission-analysis/geomagnetic-integral]]
- **First sky scan** — max $K$ is limb-grazing; "along the field" is low
  only at high magnetic latitude; range ×9 at the equator, ×4000 at 60°.
  → [[02-mission-analysis/pointing-optimization]]
- **Research pass** — no keV follow-up to Yamamoto; GECOSAX; NXB vs COR
  practice; analytic CXB/GRXE; sources added.
  → [[04-plan/literature-review]] §6
- **Decisions** D19 (stdlib toolkit), D20 (Earth-facing boresight
  allowed, thermal deferred), D21 (numpy/scipy/astropy library by topic,
  notebook run file; supersedes D19). → [[decisions]]
- **Questions** A4 closes Q17 (plasma); Q21 frames-through-occultation;
  Q22 limb background. Q4, Q16, Q18 annotated. → [[open-questions]]
- **Student notes** — Stage 2 uses the repo field model; Stage 3–4 checks
  corrected; mentor guide points at the reference implementations.
  → [[05-student/project-pathway]], [[05-student/mentor-guide]]
- **Baseline** — ConOps constraint table updated with the PI's answer on
  Earth-facing pointing. → [[00-baseline/darkness-conops]]

## Repo

`CLAUDE.md` language and layout rules rewritten for D21; `README.md`
layout and quick start; `data/bfield/igrf14coeffs.txt` added;
`requirements.txt` unchanged (numpy, scipy, astropy, matplotlib).

## Next

Pointing schedules (two targets, field-tracking), the per-target
$\rho[K, R_c]$ sky map, radiator/Sun keep-outs with a body geometry,
NFW column density, the meridian-plane geometry figure, CHAOS.

## Links

- previous log: [[2026-09-17-reorganization]]
- home: [[ALP]]
