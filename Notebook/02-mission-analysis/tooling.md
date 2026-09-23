---
type: note
tags: [darkness, alp, mission-analysis, tooling]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# Tooling: the simulation library

**Decision (D21, 2026-09-17): numpy/scipy/astropy library, functions on
arrays, organised by topic; the run file is a Jupyter notebook.** This
supersedes the same-day stdlib toolkit (D19), which supersedes the
2026-07-28 `skyfield`/`ppigrf` plan. The reasons for avoiding
GMAT/STK/Orekit still hold: this is a design study, the hard piece is
the line-of-sight integral, and we need pointing geometry, not attitude
control loops.

## Architecture

```
src/darknessalp/
  frames/      time, GCRS<->ITRS, Sun, Galactic     (astropy)
  orbit/       CCSDS elements -> propagate (point | j2); OEM in/out
  dynamics/    accelerations and torques — models, no integration loop
  kinematics/  body attitude (scipy Rotation), slews, steering
  pointing/    target specs, modes, condition schedules, keep-outs
  field/       IGRF-14 vectorised (lmax=1 is the dipole), magnetic coords
  geometry/    LOS integral over many rays at once, limb, umbra, FOV
  background/  CXB, GRXE, NXB proxy, bright sources
  sim/         state_table -> dict of arrays, CSV
jupyter/darkness_alp_sim.ipynb   the run file
scripts/fov_view.py              thin CLI + the reusable fov_view() axes
scripts/api_reference.py         regenerates the API reference note
```

Rules: astropy owns time and frames, scipy owns integration and
rotations, numpy owns arrays. Custom code only where no package does
the job. Functions take `(N, 3)` km / tesla / degrees and astropy
`Time`; no classes; nothing in `src/` prints or plots. Four packages,
nothing new without a reason in `requirements.txt`. No FORMS.

Every public function, with its signature and one-line contract, is
in [[api-reference]] — generated from the docstrings by
`scripts/api_reference.py`, with a test that fails if it goes stale.

## Known-answer checks (58 tests pass)

The full scheme — invariants, published-number gates, regression pins —
is in [[testing]].

| Check | Value |
|---|---|
| IGRF vs legacy IGRF-13 at 2020, 45N 75W 420 km | $B_r$ −40998 (−40999), $B_\phi$ −3173 nT |
| dipole ≡ `igrf_field(lmax=1)` | exact |
| surface field: equator/Greenwich, pole, SAA | 31.9, 56.6, <23 µT |
| LOS zenith / nadir closed forms at the magnetic equator, 420 km | 83.3 / 11.3 T m to 1 % |
| along-axis from the equator | 2× zenith |
| reversal ray | running total dips |
| $L_{\max}$ 10 vs 20 $R_E$ | within 2 % |
| period at 420 km; SSO node rate at 500 km / 97.4° | 92.97 min; 0.9856°/d |
| frames: ECEF rotates 90° in 6 h; GC at RA 266.405°; Sun at equinox | pass |
| cone quadrature weights; projection radius = true angle | pass |
| state table, one orbit, CSV round trip | pass |

Frames are now GCRS/ITRS via astropy, so the earlier "equinox of date"
caveat is gone. Latitude is geocentric (`frames.spherical`).

**One orbit setup (D27).** Osculating CCSDS OPM elements →
`elements_to_state` → `propagate(..., gravity="point" | "j2")` on GCRF
axes → `write_oem`. Quote altitude above the WGS84 equatorial radius
($a = 6378.137 + h$ km), not the IGRF sphere. Elements are osculating:
a circular orbit at epoch picks up a small J2 eccentricity and a mean
semi-major axis ~6 km off, so it drifts ~900 km/day in-track from a
mean-element orbit with the same numbers. One day with J2 takes
0.2 s.

## Speed

625 full-IGRF rays × 101 steps in 0.18 s (one vectorised call). A
1440-sample day with the full field and one ray per sample runs in
about a minute in the notebook; a 61×61 boresight map is instant.

## First run (notebook, 2026-09-17)

GC as a fixed inertial target, ISS-like 420 km / 51.6°, 2027-05-01, one
day at 60 s: 38 % umbra, 39 % occulted, 513 usable sky frames.
$K$ from 0 to $8\times10^4$ T² m². **corr($K$, $R_c$) = +0.74,
corr($K$, limb angle) = −0.87** on the usable frames. The nominal
target is strongly confounded on both counts, which is the premise of
[[pointing-optimization]] made quantitative.

## Pointing system (same day, later)

`pointing/targets.py` (inertial, solar-system, orbit-based, field-based
specs), `pointing/modes.py` (primary + roll rule → attitude),
`pointing/schedule.py` (condition → mode), `kinematics/steering.py`
(rate-limited chase, no dynamics). The ritual is in [[pointing-system]].
The notebook now schedules `gc` in umbra and `anti_sun` in sunlight and
steers at 1.5°/s. 37 tests.

Two functions were named `direction` in different topics; they are now
`pointing.target_direction` (a spec to a sky direction) and
`geometry.offset_direction` (an angular offset within the field of
view).

## Still to write

`dynamics/attitude.py` and radiator/Sun keep-outs with a real body
geometry (Q4), the per-target $\rho[K, R_c]$ sky map, a rule-emitting
schedule optimiser, CHAOS comparison, the meridian-plane geometry
figure.

## History

2026-07-28: `skyfield` + `ppigrf` recommended. 2026-09-17 morning:
stdlib one-function-per-file toolkit built and validated (D19).
2026-09-17 afternoon: rebuilt on numpy/scipy/astropy with topic folders
so the student writes little code and never sees an integrator (D21);
the known-answer checks carried over unchanged.

## Links

- part of [[../ALP]]
- what it computes: [[geomagnetic-integral]]
- map it serves: [[conops-physics-map]]
- cases: [[orbit-cases]]
- student view: [[../05-student/project-pathway]]
