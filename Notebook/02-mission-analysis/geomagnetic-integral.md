---
type: note
tags: [darkness, alp, mission-analysis, geomagnetic]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# The line-of-sight field integral

The one new physics module. Everything else in the chain already exists in `LimitCalculation`. This note
fixes the definition precisely enough to implement, because sign and endpoint conventions are exactly where
this kind of calculation goes wrong quietly.

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
| Internal field | IGRF-14 | `EXT` | Current release; IGRF-13 acceptable, differences negligible here |
| External field | none, initially | `ASSUME` | Tsyganenko T96/T05 as an ablation — see below |
| $L_{\max}$ | 10 $R_E$, with convergence test | `ASSUME` | $B \sim r^{-3}$, so the integral converges fast |
| Earth occultation | hard cut when the ray intersects the solid Earth | `ASSUME` | Also drives limb-avoidance |
| Atmospheric absorption | none, for rays above the limb | `ASSUME` | Revisit if limb-grazing geometries survive the trade |

**On the external field.** IGRF alone is defensible for a first pass: at a few $R_E$ the internal dipole
still dominates the total, and Yamamoto used IGRF-12 only. But the external contribution grows with
distance and correlates with space weather — which also drives the particle background. That correlation
is a systematic that could masquerade as signal, since both track geomagnetic activity. Run the ablation
(internal only vs internal+T96) early enough that it can inform the pointing strategy, not as an
afterthought.

## Convergence and cross-checks

Before trusting any output:

1. **Sanity magnitude.** Yamamoto report $(B_\perp L)^2 \sim 10^4$–$10^5$ T² m² for Suzaku-like geometry,
   i.e. $B_\perp L \sim$ 100–300 T m, with an IGRF-12 calculation every 60 s out to 6 $R_E$. Reproducing
   that magnitude in a Suzaku-like orbit is the primary validation gate for this module.
2. **Dipole limit.** For a pure dipole and a zenith-pointing observer at the magnetic equator the integral
   has a closed form; check the numerics against it.
3. **$L_{\max}$ convergence.** Vary 4 → 20 $R_E$ and confirm the integral plateaus.
4. **Sign/parity.** Field reversal along the path can cause cancellation. Confirm the code exhibits it
   (integrate through a field reversal deliberately) rather than silently taking $|B_\perp|$ inside the
   integral — a classic error that inflates the answer.

That last one deserves emphasis: $\int B_\perp ds \ne \int |B_\perp| ds$. Cancellation across field
reversals is physical and *reduces* the signal. Any implementation that never shows cancellation is wrong.

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
- consumer: [[pointing-optimization]]
- orbits: [[orbit-cases]]
