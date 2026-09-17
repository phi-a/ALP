---
type: note
tags: [darkness, alp, physics, scaling]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# Sensitivity scaling and why geometry matters

This scaling is a useful planning bound. It does not decide the schedule until background covariance and
operational losses are included.

## The scaling

The signal goes as $S \propto P_{a\to\gamma} \propto g^2 (B_\perp L)^2$. In the background-limited regime
the smallest detectable signal goes as $S_{\min} \propto \sqrt{B} \propto \sqrt{A \Omega t}$, so the
smallest *detectable fraction* improves as $(A\Omega t)^{-1/2}$. Inverting for the coupling:

$$
\boxed{\;g_{\min} \;\propto\; \frac{(A\,\Omega\,t)^{-1/4}}{B_\perp L}\;}
$$

Read the exponents:

- **Exposure and grasp enter at the fourth root.** 16× more observing time buys a factor of 2 in coupling.
- **The field integral enters linearly.** 2× more $B_\perp L$ buys the same factor of 2.

Before nuisance projection, doubling the integrated field along the line of sight has the same coupling
effect as sixteen times the observing campaign. The realized benefit can be smaller or zero if the selected
geometry also changes the background. Yamamoto took what the archive gave them; the DarkNESS case study
can test whether controlled pointing improves the residualized signal information.

## Pre-study estimate of the reach

Rough, and meant to be replaced by the actual calculation — but it sets expectations:

| Factor | Ratio vs Yamamoto | Gain in $g$ |
|---|---|---|
| Grasp (0.52 vs 0.026 cm² sr, conservative) | ~20× | 20^(1/4) ≈ 2.1 |
| Exposure (0.5–1.0 Ms vs ~0.845 Ms) | ~0.6–1.2× | ~0.9–1.04 |
| Grasp × exposure together | ~12–24× | ~1.9–2.2 |
| Effective field leverage | 1.5–2× (hypothesis) | 1.5–2 |
| Background covariance/systematics | unknown | can erase the pointing gain |

If an executable schedule really supplies the assumed field leverage without becoming collinear with the
background, the planning bracket is a total factor of roughly **2.8–4.4** in coupling. Applied only as a
conditional scaling of Yamamoto, that would put the universal-continuum example near
$g \sim (0.75$–$1.2)\times10^{-7}$ GeV⁻¹ and the Galactic-line example near
$g \sim (1.9$–$3.0)\times10^{-8}$ GeV⁻¹.

These are not projected limits. They mix unvalidated response and pointing assumptions, inherit the
parent-decay source model, and assume the background-dominated statistical scaling remains valid. The
older $2$–$3\times10^{-8}$ estimate was incorrectly described as applying to Yamamoto's cyan continuum
curve; it corresponds numerically to the stronger Galactic-line benchmark. See
[[coherence-and-mass-reach]] for why neither case extends the mass axis.

## What the scaling implies for design choices

1. **Optimise identifiability first.** Field strength is a linear lever only after its covariance with the
   background model is removed.
2. **Background reduction is worth as much as background avoidance.** $B$ enters under the same 1/4 power
   as exposure, so halving the background equals 16× the exposure only if it does not cost duty cycle —
   which it usually does. Model the trade, do not assume it.
3. **Do not chase exposure.** Extending the campaign from 500 ks to 1 Ms buys 1.19× in coupling. Extending
   it at the cost of a worse pointing distribution is a net loss.
4. **Grasp is already banked.** The 20× over Suzaku comes from the wide FOV that DarkNESS has regardless.
   Nothing in the study can improve it, and DarkNESS-2's lobster-eye optics would *reduce* Ω while raising
   $A$ — a trade worth checking if that design ever firms up, since the product is what matters.

## The caveat on the background-limited assumption

$g_{\min} \propto (A\Omega t)^{-1/4}$ assumes Poisson background dominance. Yamamoto's actual limit was
**systematics-limited** — set by how well the CXB and NXB could be modelled, not by counting statistics.
If DarkNESS lands in the same regime, exposure buys nothing at all and the whole gain has to come from the
$(B_\perp L)^2$ lever arm and background modelling. This is the strongest argument for framing the analysis
as a *correlation* measurement rather than an absolute photometric one; see
[[../03-sensitivity/method]].

## Links

- part of [[../ALP]]
- the lever: [[../02-mission-analysis/pointing-optimization]]
- numbers: [[../00-baseline/darkness-parameters]]
