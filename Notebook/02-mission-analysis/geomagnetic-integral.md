---
type: note
tags: [darkness, alp, mission-analysis, geomagnetic]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# The line-of-sight field integral

The one new physics module. This note fixes the definition precisely
enough to implement, because sign and endpoint conventions are exactly
where this kind of calculation goes wrong quietly. Implemented as
`los_field_integral` (see [[tooling]]); the gates below pass as of
2026-09-17.

## Definition

The ALP arrives from outside the magnetosphere, travels inward along the boresight, and converts somewhere
along the way; the photon continues to the detector. So the integral runs **outward from the spacecraft**
along the viewing direction $\hat n$:

$$
\mathcal{A}(\hat n, t) = \int_{0}^{L_{\max}} B_\perp(\mathbf{r}(s), \hat n)\;
e^{\,i q s}\, ds, \qquad
\mathbf{r}(s) = \mathbf{r}_{\rm sc}(t) + s\,\hat n
$$

$$
B_\perp = \left| \mathbf{B} - (\mathbf{B}\cdot\hat n)\,\hat n \right|
$$

with $P_{a\to\gamma} = (g_{a\gamma\gamma}/2)^2 |\mathcal{A}|^2$. In the coherent limit the phase drops out
and $|\mathcal{A}| \to B_\perp L$, recovering the familiar form.

Two things to get right:

- **$B_\perp$ is perpendicular to the line of sight, not to the orbit.** It is the projection of the local
  field onto the plane normal to $\hat n$. This is what makes the answer depend on pointing at all.
- **Keep the phase inside the integral.** The coherent shortcut is fine for broad scans, but the knee region
  is exactly where the phase matters, and the knee is where the limit curve's shape lives. Implement the
  full integral; use the shortcut only as a validated fast path.

## Endpoint and model choices

| Choice | Baseline | Tag | Note |
|---|---|---|---|
| Internal field | IGRF-14, `lmax` 13 (1 = tilted dipole for scans) | `EXT` | `data/bfield/igrf14coeffs.txt`, valid to 2030 |
| External field | none | `ASSUME` | Tsyganenko T96/T05 as an ablation — see below |
| Plasma | none | `DERIV` | $\omega_{\rm pl}^2/m_a^2 \sim 4\times10^{-6}$ at the knee; A4 in [[../open-questions]] |
| $L_{\max}$ | 10 $R_E$ | `ASSUME` | truncation costs 1 % (83.4 → 82.4 T m zenith); 20 $R_E$ recovers it |
| Earth occultation | ray ends at the surface | `ASSUME` | the path from surface to spacecraft still converts: 11 T m nadir at 420 km |
| Atmospheric absorption | none above the limb | `ASSUME` | revisit if limb-grazing geometries survive the trade |

**On the external field.** IGRF alone is defensible for a first pass: at a few $R_E$ the internal dipole
still dominates the total, and Yamamoto used IGRF-12 only. But the external contribution grows with
distance and correlates with space weather — which also drives the particle background. That correlation
is a systematic that could masquerade as signal, since both track geomagnetic activity. Run the ablation
(internal only vs internal+T96) early enough that it can inform the pointing strategy, not as an
afterthought.

## Convergence and cross-checks

Status 2026-09-17, all in `tests/test_los_field_integral.py`:

1. **Sanity magnitude.** Yamamoto report $B_\perp L \sim$ 100–300 T m
   for Suzaku-like geometry. Our dipole scan at 420 km gives 5–340 T m
   depending on direction and magnetic latitude (table in
   [[pointing-optimization]]). Passes.
2. **Dipole closed forms.** Zenith at the magnetic equator:
   $B_0 R_E^3/2r_0^2 = 83.3$ T m; nadir through the Earth:
   $B_0 R_E (1 - R_E^2/r_0^2)/2 = 11.3$ T m. Both to 1 %.
3. **$L_{\max}$ convergence.** 5 → 10 → 20 $R_E$: 79.5, 82.4, 83.4 T m.
   Plateau confirmed; 10 $R_E$ adopted.
4. **Sign/parity.** A ray from $\lambda_m = 15°$ looking south along the
   axis crosses the equatorial plane where $B_\rho$ flips: the running
   total rises to 18 T m, falls through zero, ends at 161 T m against a
   naive $\int|B_\perp|ds = 196$ T m. Cancellation is real and the code
   shows it.

$\int B_\perp ds \ne \int |B_\perp| ds$. Any implementation that
never shows the dip in gate 4 is wrong.

## Field of view

$P$ must be integrated over the 20° cone, not evaluated on the boresight — see the within-FOV gradient
discussion in [[../01-physics/alp-signal-chain]]. Practical approach: evaluate on a coarse grid over the
aperture (start with ~19 points, hex-packed) and check convergence against a finer grid on a few
representative geometries.

## Outputs this module must produce

For each candidate orbit and time step, a map over accessible sky directions of:

- $|\mathcal{A}|^2$, FOV-averaged, per energy (the phase makes it energy-dependent)
- the coherent approximation, for speed comparison
- accessibility flags: umbra, Earth-limb angle, Sun angle, SAA, radiator constraint

That data cube is the input to [[pointing-optimization]].

## Links

- part of [[../ALP]]
- physics: [[../01-physics/alp-signal-chain]]
- implementation: [[tooling]]
- consumer: [[pointing-optimization]]
- orbits: [[orbit-cases]]
