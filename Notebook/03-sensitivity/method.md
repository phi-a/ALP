---
type: note
tags: [darkness, alp, sensitivity, method]
created: 2026-07-28
updated: 2026-09-08
status: active
---

# Sensitivity method

How the projected limit gets computed, and how much of it already exists.

## Reuse from the sterile-neutrino chain

`darkmatter/LimitCalculation` already implements, for the DarkNESS X-ray line search:

`background template → Si QE → Gaussian smearing at σ_E → counts in window → ON/OFF photometry → limit`

(`darkness.py`, `sensitivity*.py`, `src/background.py`, `src/physics.py`). The ALP study reuses the back
half unchanged. Two things change at the front:

1. **The source term** contains the linked Milky Way feature and
   extragalactic continuum, multiplied by $P_{a\to\gamma}$.
2. **The discriminant** is a correlation with
   $(B_\perp L)^2$ across frames.

Before reuse, reconcile `area_cm2 = 8.0` and `efficiency = 0.20` against the published 12 cm² and ~50 %
masking. See [[../00-baseline/darkness-parameters]] and [[../open-questions]].

## The statistical model

Frames indexed by $i$ (time/pointing), energy bins by $j$:

$$
\mu_{ij} = a\,x_i\,s_j + b_{ij}, \qquad x_i = (B_\perp L)^2_i
$$

with $s_j$ the response-folded joint ALP spectral template and $b_{ij}$ the
background model. If the parent decay rate is independent of the photon
coupling, the fitted source amplitude satisfies

$$
a\propto g_{a\gamma\gamma}^{2}
\frac{f_\chi\mathcal B_{aa}}{\tau_\chi}.
$$

The earlier $g_{a\gamma\gamma}^{4}$ statement was incorrect. Profile over the
background normalizations and report the limit on the combined amplitude
before translating it to a conditional coupling value.

The Milky Way component additionally carries $S_\phi(l,b)$ into its template.
The extragalactic component carries no leading sky-density factor.

## Why it must be a correlation measurement

Yamamoto's limit was **systematics-limited**, not statistics-limited: it came from the absence of a
correlation between residual background and $(B_\perp L)^2$, after fitting CXB, NXB, and Milky Way halo
components. Absolute photometry cannot do better, because the CXB normalisation is uncertain at the level
of the entire signal being sought.

This is the whole reason the pointing scheme is the deliverable. The measurement's power comes from
$x$ varying while everything else is held fixed. See [[../02-mission-analysis/pointing-optimization]].
Reporting a purely statistical projection would overstate the reach, possibly badly.

## Background components to model

| Component | Treatment | Correlates with $x$? |
|---|---|---|
| CXB | Fitted normalisation, spectral shape from literature | No, the key discriminant |
| NXB / particle | From DarkNESS radiation modelling, geomagnetic-latitude dependent | **Yes, potentially**, the main confounder |
| Cherenkov / low-energy hits | `DN-V` p. 4795, LEO modelling ongoing | Below band, but affects masking |
| Earth albedo, limb | Excluded by pointing constraints | Yes if limb angle correlates with pointing |
| SWCX | Anti-Sun scheduling and solar-wind proxies as nuisance | Seasonal, weakly |
| Milky Way halo / Galactic diffuse | Sky-position dependent | Enters the Milky Way component and its backgrounds |

The NXB row is the one that decides the result. Particle background depends on geomagnetic cutoff
rigidity, which depends on position, which also drives $B_\perp L$. **That correlation is the central
systematic of this entire study** and must be quantified before any limit is quoted.

## Validation gates

Do not report a DarkNESS number until:

1. The field integral reproduces Yamamoto's $(B_\perp L)^2 \sim 10^4$–$10^5$ T² m² in Suzaku-like geometry
   ([[../02-mission-analysis/geomagnetic-integral]])
2. The full chain, run with Suzaku's grasp, exposure, and fields, **reproduces Yamamoto's published
   limits** ($3.3\times10^{-7}$ and $8.4\times10^{-8}$ GeV⁻¹) to within a factor of ~2
3. Injected signals at known $g$ are recovered without bias
4. The NXB-vs-$x$ correlation has been quantified, not assumed away

Gate 2 is the one that makes the result publishable: it demonstrates the pipeline against a published
analysis before extrapolating to a new instrument. The Figure 7 replication in `darkmatter/ALP` already
provides the target curve, digitised and validated.

## Output hierarchy

1. A source-agnostic converted-brightness or $g^2I_a$ limit.
2. A constraint on the combined parent-decay amplitude.
3. A conditional DarkNESS curve on the Yamamoto Figure 7 axes, plotted as a
   line because it is a projected sensitivity.
4. A comparison with current constraints expressed under compatible source
   assumptions.

## Links

- part of [[../ALP]]
- the result: [[result]] (gates 1-3 met 2026-09-24; gate 2 at a factor 2.3)
- source models: [[../01-physics/alp-signal-chain]]
- derivation contract: [[../01-physics/detection-channel-derivation-contract]]
- scaling: [[../01-physics/sensitivity-scaling]]
- pointing: [[../02-mission-analysis/pointing-optimization]]
