---
type: result
tags: [darkness, alp, geometry, conversion, occultation, block-a]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# 2026-09-24 — where an occulted ray ends

An occulted line of sight must end where a converted photon can no
longer reach the detector. `geometry.path_end_km` ends it at the
Earth's surface. This note states where it should end and what the
choice changes.

## The boundary

ALPs cross the Earth; photons do not. A photon converted beyond the
Earth never arrives. A photon converted on the near side arrives only
if the air between the conversion point and the detector is
transparent to it. The ray therefore ends at the altitude where the
atmosphere becomes opaque to 1–10 keV photons, not at the surface.

`[DH06]` §2 gives the scale: the absorption length of 4 keV X-rays is
about 10 cm at sea level and scales inversely with pressure; above
150 km the pressure is below $10^{-10}$ atm and the absorption length
exceeds $10^6$ km. So 150 km bounds the transition from below. The
true boundary is higher for a ray far from nadir, whose slant path
through each layer is longer, and higher for 1 keV than for 10 keV,
since the photoabsorption cross-section falls roughly as $E^{-3}$.

## What it changes

Reference day (420 km, 51.6°, dipole field, 10-min cadence; 57 of 144
frames occulted). Ending the ray at 150 km instead of the surface:

| Rays | $K_{150}/K_{\rm surface}$ |
|---|---|
| all occulted frames, median (range) | 0.37 (0.17–0.43) |
| the two occulted science-mode frames | 0.32 |
| a pure nadir ray at 420 km | 0.39 ($\sqrt K$: 0.63) |

Sky rays are unchanged. The state table's `k_t2m2` for occulted frames
is therefore too large by a factor of about 2.7. Those frames are the
night-Earth $K$-off control (Q21): the on/off contrast is larger than
the table says, and a fit that uses the table's template for the off
frames carries a template error of that size.

## Close

The endpoint is an altitude that depends on nadir angle and energy and
lies above 150 km; the surface is wrong for every occulted frame.
**Applied 2026-09-24 (D32):** `path_end_km` ends every ray at the
150 km shell by default (`end_alt_km`); a ray grazing below 150 km is
truncated there without being flagged occulted. The angle and energy
dependence of the true boundary remains Q23, tagged `ASSUME`, and
moves the control frames by less than the 2.7 just removed.

## Links

- derivation: [[01-physics/block-a-conversion]] §4
- open: [[open-questions]] Q21, Q23
- code: `geometry.path_end_km`, `geometry.los_field_integral`
