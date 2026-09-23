---
type: result
tags: [darkness, alp, geometry, signal]
created: 2026-09-23
updated: 2026-09-23
status: active
---

# 2026-09-23 — the conversion kernel averaged over the aperture

`geometry.fov_field_integral` averages $|\mathcal A|^2$ over the 20°
cone with the equal-area quadrature of `cone_directions` (19 rays,
ray 0 the boresight). `sim.state_table` now carries `k_fov_t2m2`
next to the boresight `k_t2m2`, plus `fov_occ_frac`, the weighted
share of the aperture that looks at the Earth.

## Why

For the isotropic (extragalactic continuum) channel the whole
direction and time dependence of the ALP signal is the conversion
kernel; the source is a constant. So the signal a schedule collects
is $\sum_i \langle K\rangle_i\,\Delta t_i$ up to a normalisation
that cancels in any schedule comparison. The boresight value is not
what the detector measures across a 20° field
([[01-physics/alp-signal-chain]], within-FOV gradient).

## Result — reference scenario, dipole, 10-min cadence

| | |
|---|---|
| median $\langle K\rangle / K_{\rm boresight}$ (sky samples) | 1.017 |
| range | 1.011 – 1.266 |

The aperture average sits 1–2 % above the boresight for most of the
schedule and up to 27 % above it when the field is pointed near the
limb, where $B_\perp L$ changes fastest across the cone. Pinned in
`test_scenario_regression.test_fov_gradient`.

## Cost

33 ms per sample at IGRF degree 13 (19 rays) against 14 ms for one
ray; the day-long notebook run goes from ~20 s to ~50 s.

## Next

- put `k_fov_t2m2` beside `cutoff_gv`, GRXE and `umbra` and test
  whether the kernel modulation is separable from theirs
- the Milky Way line reuses this quadrature with the NFW column
  density inside the weighted sum: $\langle D\cdot K\rangle$

## Links

- part of [[ALP]]
- decision: [[decisions]] D21, D22
- field integral: [[02-mission-analysis/geomagnetic-integral]]
