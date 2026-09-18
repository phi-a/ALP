---
type: note
tags: [darkness, alp, tooling, testing]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# How we test the simulation

```powershell
python -m pytest
```

58 tests, ~6 s, no environment setup (`pytest.ini` puts `src` on the
path and turns `DeprecationWarning` into an error). **Do not use
`python -m unittest discover`** — it silently collects zero from
pytest-style files, which is how 18 tests went unnoticed for a day.

Nothing here checks that the code runs. Everything checks that it
gets a number somebody can verify independently. Five layers, weakest
claim first.

## 1. Known answers — `test_field`, `test_frames`, `test_orbit`, `test_geometry_*`

A closed form, a published constant, or a hand calculation, next to the
value the code returns. The line-of-sight integral has four of these:
the zenith and nadir dipole closed forms, the $L_{\max}$ plateau, the
cancellation dip through a field reversal, and the phase reducing the
amplitude.

These are the student's answer key. If one fails, read the physics, not
the test.

## 2. Invariants — `test_invariants`

Properties that hold whatever the inputs, so they catch what a
single-point check cannot:

- two-body propagation conserves energy and $|h|$ to 1 part in $10^9$;
  under J2 it conserves $h_z$ instead (axisymmetric, not central)
- body axes stay orthonormal; the boresight stays perpendicular to the
  radiator normal; steering never exceeds its rate limit
- $|B|$ is the same in ECI and ECEF; truncation error falls with `lmax`
- occultation from `path_end_km` agrees with a negative `limb_angle` —
  two independent routines that must never disagree
- the integral is linear in the field and independent of ray ordering
- the field-of-view average sits within 35 % of the boresight value

## 3. Cross-checks — inside `test_field`

IGRF against an independent implementation at four points (3 nT, which
is the IGRF-13→14 revision of the 2020 epoch, not a code difference).
Frames and the Sun come from astropy, so they are the cross-check.

## 4. Published-number gates — `test_validation_gates`

The layer that decides whether the physics is right at all. Each test
cites its source:

| Gate | Number |
|---|---|
| Suzaku-like geometry, 570 km / 31°, random sky pointings | median $(B_\perp L)^2 = 1.3\times10^4$ T² m², inside Yamamoto's reported $10^4$–$10^5$; 59 % of pointings land in that band |
| Hand calculation $B_0 R_E/2$ | ~100 T m |
| IGRF surface field: equator, pole | 31.9, 56.6 µT |
| Störmer cut-off at the magnetic equator | 14.9 GV |
| CXB in the DarkNESS cone | 9.9 ct s⁻¹ |
| Orbital periods, 420 and 500 km | 92.97, 94.6 min |
| Sun-synchronous node rate | 0.9856°/day |

The Suzaku gate is the one that matters: it is the primary validation
gate named in [[geomagnetic-integral]], and it passes.

## 5. Regression — `test_scenario_regression`

Runs the whole ritual (orbit → conditions → mode schedule → steering →
state table) for one reference day and pins the answers: 144 samples,
52 in umbra, 57 occulted, 30 slewing, 37 usable science frames, median
75 T m, corr($K$, $R_c$) $= +0.894$, corr($K$, limb) $= -0.987$. Plus a
determinism check that a second run is identical.

These pins are *descriptions, not requirements*. When one moves,
recompute it deliberately and say why in the commit — never edit it to
make the suite green.

## Documentation is tested too — `test_api_reference`

Every public name appears in [[api-reference]], every function has a
docstring, and regenerating the note reproduces it byte for byte.

## What this does not cover

- **The notebooks.** `jupyter/darkness_alp_sim.ipynb` and
  `Yamamoto2020_Fig7.ipynb` are run by hand. The scenario regression
  covers the same sequence at coarse cadence, so a broken notebook is
  usually a broken cell, not broken physics.
- **The FOV figure.** Rendering is checked by looking at it.
- **Backgrounds beyond shape.** `grxe_brightness` and `nxb_proxy` are
  `ASSUME` models; the tests fix their shape, not their truth.
- **External field, plasma, atmosphere.** Not modelled, so not tested.

## What the tests have caught

Worth recording, because it is the argument for the layers:

1. A silent `unittest` collection gap hiding 18 tests.
2. A `DeprecationWarning` in `steer` that becomes an error in a future
   numpy, from a one-element rotation stack.
3. The API reference regenerating differently every run, because a
   default argument rendered as a memory address.
4. **`circular_orbit` measured altitude above the IGRF reference sphere
   (6371.2 km) rather than the WGS84 equatorial radius (6378.137 km)**,
   giving 92.83 min at 420 km where the published ISS period is
   ~92.97. Conflating the geomagnetic reference sphere with the orbital
   one is exactly the silent-constant error [[tooling]] warns about, and
   only a published-number gate could have found it.

## Links

- part of [[../ALP]]
- what is tested: [[tooling]], [[pointing-system]], [[api-reference]]
- the gate in 4: [[geomagnetic-integral]]
- student answer keys: [[../05-student/project-pathway]]
