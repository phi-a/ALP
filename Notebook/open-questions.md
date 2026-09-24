---
type: note
tags: [darkness, alp, open-questions]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# Open questions

Blocking items first. Each carries what it blocks, so the cost of leaving it open is visible.

## Blocking

| # | Question | Blocks | Who can answer |
|---|---|---|---|
| Q14 | Does any benchmark allowed by current invisible-decay and $g_{a\gamma\gamma}$ constraints produce a detectable DarkNESS count rate? **Answered 2026-09-24: no.** The 90 % limit sits $4\times10^5$–$2\times10^6$ above $\Theta_{\max}$ over 187 days, statistical, before systematics — [[01-physics/block-d-claim]]. Disposition: Revise, [[decisions]] D31 | Scientific motivation and permission to optimize the mission | Primary-literature synthesis plus source-to-count calculation |
| Q15 | Can the Milky Way and extragalactic source normalizations be reproduced from a common derivation without a fitted scale? | Every mission sensitivity and coupling translation | Derivation review against Yamamoto and Dror et al. |
| Q1 | Is the 20° FOV a **full cone** (half-angle 10°) or a half-angle? **Resolved 2026-09-24: full cone, half-angle 10°**; the 40° is the obstruction keep-out — [[00-baseline/skipper-ccd]] | Grasp, and therefore every sensitivity number, linearly | DarkNESS team / aperture drawing |
| Q2 | Why does `LimitCalculation` use 8 cm² and 20 % when the paper says 12 cm² and ~50 % masking? | Reuse of the existing chain; a 1.5× area error propagates as 1.1× in $g$ | Original author of that chain |
| Q3 | Which orbit is manifested — ISS-like, SSO noon/midnight, or SSO dawn/dusk? | Which of the three cases is primary; dawn/dusk breaks umbra-only observing | Launch manifest, mid-2026 |
| Q4 | Which body axis does the payload aperture look along, and where are the radiator panels? | Whether a given science pointing is compatible with the radiator and Sun constraints. Earth-facing is not forbidden (D20) | Fig. 8 / mechanical ICD |

Q1 and Q2 are both answerable today by asking a person. They should be resolved before any number is
quoted, because both scale the final answer directly.

Q3 does not block the work — the study should carry all three cases and produce a ranking — but it does
determine which result is the headline.

## Important, not blocking

| # | Question | Note |
|---|---|---|
| Q5 | Does the ALP analysis gain from sunlit observing (Sun kept out of the aperture), or does it also go umbra-only? | Not required by the mission (PI, 2026-09-24; D30); a trade. Costs of sunlit frames: solar X-ray, optical loading, warmer MCM. If relaxable, duty cycle roughly doubles — and it is the difference between viable and not under dawn/dusk SSO. See [[decisions]] |
| Q6 | Slew rate, settle time, momentum management limits | Bounds how aggressive a scan law can be; an on/off pairing strategy needs slews within an orbit |
| Q7 | Does NXB correlate with $(B_\perp L)^2$, and how strongly? | **The central systematic.** Both track geomagnetic position. Quantify before quoting a limit — [[03-sensitivity/method]] |
| Q8 | Can the within-FOV brightness gradient be used as a discriminant? | Suzaku could not do this; DarkNESS's 20° cone might. Needs a statistics study |
| Q9 | Is any dedicated observing time obtainable, or is this strictly parasitic? | Determines whether the optimised schedule is a recommendation or a fantasy |
| Q10 | DarkNESS-2 lobster-eye optics — parameters? | Out of scope until the design firms up. Would raise $A$ and lower $\Omega$; only the product matters. See [[decisions]] |
| Q11 | Is the SmallSat result strictly a parasitic current-flight analysis, or may it compare a bounded dedicated schedule as a DarkNESS-class case study? | Determines the claim language and whether optimized pointing is a recommendation or a counterfactual trade |
| Q12 | Which source channel wins at count level: Galactic line or cosmological continuum? | Prevents the project from choosing pointing freedom over spectral identifiability without evidence |
| Q13 | Which in-frame and housekeeping quantities can act as particle-background proxies? | Determines whether the conversion kernel is identifiable and what telemetry/calibration requirements follow |
| Q16 | Is IGRF alone accurate enough for the useful path, or are external magnetosphere and space-weather models required? | Conversion uncertainty and possible covariance with particle backgrounds. IGRF-14 adopted (D19); the T96 ablation is still owed |
| Q18 | Where should each ray terminate: fixed Earth radii, magnetopause, or a field-model boundary? | Absolute conversion normalization and mass reach. 10 $R_E$ adopted; truncation costs 1 % ([[02-mission-analysis/geomagnetic-integral]]) |
| Q19 | Which existing searches constrain the same product $g_{a\gamma\gamma}^{2}f_\chi\mathcal B_{aa}/\tau_\chi$? | Claim of scientific novelty |
| Q20 | What source broadening is resolvable after the flight-like skipper-CCD redistribution? | Whether the Milky Way feature supplies meaningful spectral discrimination |
| Q21 | Do science frames continue through Earth occultation, and can the night-Earth frame serve as the $K$-off / NXB control? | Whether the free on/off pair in [[02-mission-analysis/conops-physics-map]] exists; a requirement to hand the team (D20) |
| Q22 | What is the Earth-limb / atmospheric X-ray background as a function of limb angle, day and night? | The maximum-$K$ directions are limb-grazing, so this covariate is correlated with signal by construction ([[02-mission-analysis/pointing-optimization]]) |
| Q23 | Where should an occulted ray end: the Earth surface (now) or the altitude, near 150 km, below which the atmosphere absorbs keV X-rays? | The $K$-off control frames (Q21). Ending at 150 km lowers occulted-frame $K$ to a median 0.37 of the surface value on the reference day, so the state table overstates it ~2.7x — [[2026-09-24-occulted-ray-endpoint]] |

## Answered

| # | Question | Answer | Date |
|---|---|---|---|
| A1 | Does the ALP analysis require pointing at the Galactic Centre? | **No.** The extragalactic component is isotropic to leading order. The linked Milky Way component does scale with dark-matter column density and benefits from GC pointing | 2026-07-28, clarified 2026-09-08 |
| A2 | What coherence mass should be used? | Compute from our own $L$; do **not** inherit Yamamoto's text value of 3.3×10⁻⁶ eV, which is inconsistent with their own figure and stated geometry. See [[01-physics/coherence-and-mass-reach]] | 2026-07-28 |
| A3 | Are the incident keV ALPs the cold dark matter itself? | **No.** In the reference channel they are relativistic daughters of a heavier dark-matter parent. A coupling-only curve is conditional on the parent-decay model | 2026-09-08 |
| A4 (was Q17) | Which ionosphere/plasmasphere model is needed for the phase? | **None, at first order.** Worst-case $n_e = 10^6$ cm⁻³ gives $\omega_{\rm pl} = 3.7\times10^{-8}$ eV against a coherence knee near $2\times10^{-5}$ eV at 3 keV: $\omega_{\rm pl}^2/m_a^2 \sim 4\times10^{-6}$. Revisit only for $m_a \lesssim 10^{-7}$ eV | 2026-09-17 |

## Links

- part of [[ALP]]
- decisions taken: [[decisions]]
