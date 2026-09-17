---
type: note
tags: [darkness, alp, mission-analysis, tooling]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# Tooling: the building-block scripts

**Decision (D19, 2026-09-17): small stdlib scripts written for this
project, one function per file, each with a known-answer test.** This
supersedes the 2026-07-28 recommendation of `skyfield` + `ppigrf`, kept
below as history. The reasons for avoiding GMAT/STK/Orekit still hold.

## Why not an astrodynamics platform

This is a design study, not operations: we need the distribution of
accessible $K=(B_\perp L)^2$ over a representative year, not a
spacecraft's position to the kilometre. The one hard piece — the
line-of-sight field integral — is custom work on any platform. We need
pointing geometry, not attitude dynamics. No manoeuvres, no covariance.

The one place fidelity matters is **J2 nodal regression**: without it a
sun-synchronous orbit does not stay sun-synchronous and the eclipse trade
in [[orbit-cases]] is wrong. It is one line in `circular_orbit`.

## Rules

- `src/darknessalp/`: stdlib, one function per file, file name = function
  name, one-line docstring, a `tests/test_<name>.py` with a number the
  student can check by hand. The trig and the integral are the teaching
  content, so they are not hidden in a package.
- `numpy`, `scipy`, `astropy`, `matplotlib` are allowed where they
  genuinely simplify: the analysis layer (maps, state table), `plots/`,
  and as oracles in tests. Keep the count low; new ones go into
  `requirements.txt`.
- No FORMS in the student path. It is the mentor's independent
  cross-check, later. The legacy numpy `bfield/` and `yamamoto/` code is
  also oracle-only.

## What exists (2026-09-17)

| File | Returns | Check that passes |
|---|---|---|
| `julian_date`, `gmst` | JD; GMST deg | J2000 = 2451545.0, 280.461°; astropy to 0.01° |
| `circular_orbit` | ECI r, v; J2 node rate | 92.8 min at 420 km; SSO 0.9856°/d at 97.4°; ISS −5°/d |
| `eci_to_ecef`, `ecef_to_eci`, `ecef_to_spherical` | rotations; geocentric lat, lon, r | round trips |
| `sun_direction` | ECI unit vector | astropy, equinox of date, to 0.007° |
| `in_umbra`, `earth_limb_angle` | flags, degrees | Earth angular radius 69.74° at 420 km |
| `load_igrf` | IGRF-14 `{(n, m): (g, h)}` nT, to 2030 | epoch values; SV extrapolation |
| `schmidt_legendre` | $P_n^m$, $dP/d\theta$ to n=13 | closed forms n≤2; finite difference 1e-8 |
| `igrf_field(lmax)`, `dipole_field` | tesla, ECEF | legacy IGRF-13 to 3 nT; `lmax=1` ≡ dipole; SAA 22 µT, pole 57 µT |
| `field_eci` | tesla, ECI | frame-independent magnitude |
| `los_field_integral` | $\|\mathcal A\|$ T m, running total, occulted flag | closed forms 83.3 (zenith) and 11.3 (nadir); reversal dips; 20 ms per full-IGRF ray |
| `magnetic_latitude`, `cutoff_rigidity` | $\lambda_m$; Störmer $R_c$ GV | 80.9° at the pole; 14.9 GV |
| `radec_to_eci`, `galactic_to_radec`, `radec_to_galactic` | sky frames | GC 266.405°, −28.936°; astropy to 1e-3° |
| `fov_axes`, `project_to_fov`, `angular_separation`, `earth_limb_directions` | satellite-view offsets, degrees | radius = true angle from boresight |
| `bright_sources` | 18 brightest 2–10 keV sources, `ASSUME` fluxes | positions checked |
| `plots/fov_view.py` | what the boresight sees: Earth, Sun, Galaxy, sources, $K$ map | figures in `outputs/` |

51 tests: `python -m unittest discover -s tests`.

**Frame convention.** ECI is the mean equator and equinox *of date* —
what GMST rotates into ECEF, and what the Almanac Sun formula gives.
J2000 catalogue positions differ by ≤0.4° over 2026–2028; ignored for a
20° cone, noted here so nobody hunts for it. Latitude is geocentric;
geodetic differs by <0.2°.

**Speed.** A full-IGRF ray (200 steps) costs 20 ms; a dipole ray 1 ms.
A 25×25 direction grid with the dipole is 0.6 s, so sky maps at one
epoch are interactive and a year at one orbit per week is minutes. Use
`lmax=1` for scans, `lmax=13` for final numbers.

## Still to write

`fov_directions` (cone quadrature), `dm_column_density` (NFW $S_\phi$),
`cxb_intensity`, `grxe_intensity`, `nxb_proxy`, `state_table`, and the
per-target $\rho[K, R_c]$ map. Then the two remaining figures: the
meridian-plane geometry diagram and the instant full-sky $K$ map.

## Validation gates

The two cheap gates from the original plan both pass: IGRF against an
independent implementation (3 nT, the IGRF-13→14 revision of the 2020
epoch) and the SAA appearing in the right place. Frames are checked
against astropy. What LLM-written orbital code gets wrong silently is the
frame; the tests above are what make generated code safe here.

## History

2026-07-28: recommended `skyfield` for frames and `ppigrf` for the field,
with numpy. Superseded by D19: the student learns more from fifteen lines
of trigonometry with a known answer than from a library call, and the
pure-Python IGRF turned out fast enough.

## Links

- part of [[../ALP]]
- what it computes: [[geomagnetic-integral]]
- map it serves: [[conops-physics-map]]
- cases: [[orbit-cases]]
- student view: [[../05-student/project-pathway]]
