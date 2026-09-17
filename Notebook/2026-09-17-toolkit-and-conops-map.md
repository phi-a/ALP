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
- **Toolkit** — 27 stdlib one-function scripts in `src/darknessalp/`
  (orbit with J2, time, frames, IGRF-14, dipole, line-of-sight integral
  with occultation, umbra, limb, Sun, magnetic latitude, cutoff rigidity,
  sky frames, FOV projection, bright sources); 51 tests incl. astropy and
  legacy-IGRF oracles; `plots/fov_view.py`.
  → [[02-mission-analysis/tooling]]
- **Field-integral gates pass** — closed forms, $L_{\max}$ plateau,
  reversal cancellation. → [[02-mission-analysis/geomagnetic-integral]]
- **First sky scan** — max $K$ is limb-grazing; "along the field" is low
  only at high magnetic latitude; range ×9 at the equator, ×4000 at 60°.
  → [[02-mission-analysis/pointing-optimization]]
- **Research pass** — no keV follow-up to Yamamoto; GECOSAX; NXB vs COR
  practice; analytic CXB/GRXE; sources added.
  → [[04-plan/literature-review]] §6
- **Decisions** D19 (toolkit rules, IGRF-14, frames), D20 (Earth-facing
  boresight allowed, thermal deferred). → [[decisions]]
- **Questions** A4 closes Q17 (plasma); Q21 frames-through-occultation;
  Q22 limb background. Q4, Q16, Q18 annotated. → [[open-questions]]
- **Student notes** — Stage 2 uses the repo field model; Stage 3–4 checks
  corrected; mentor guide points at the reference implementations.
  → [[05-student/project-pathway]], [[05-student/mentor-guide]]
- **Baseline** — ConOps constraint table updated with the PI's answer on
  Earth-facing pointing. → [[00-baseline/darkness-conops]]

## Repo

`CLAUDE.md` language rule updated (packages allowed, minimised);
`README.md` layout; `data/bfield/igrf14coeffs.txt` added;
`requirements.txt` unchanged. Uncommitted on
`claude/darkness-alp-simulation-d0c85c`.

## Next

Cone quadrature, background columns (CXB, GRXE, NFW column, NXB proxy),
the state table, the per-target $\rho[K, R_c]$ sky map, and the two
remaining figures (meridian-plane geometry; instant full-sky $K$ map).

## Links

- previous log: [[2026-09-17-reorganization]]
- home: [[ALP]]
