---
type: result
tags: [darkness, alp, source, nfw, cab, signal]
created: 2026-09-23
updated: 2026-09-23
status: active
---

# 2026-09-23 — source models: the halo column, and the cosmic ALP background checked and retired

New topic `source/`. With the conversion kernel already in `geometry/`,
the two surviving ALP channels in [[02-mission-analysis/conops-physics-map]]
now have their direction-dependent part in the library. The third, the
cosmic ALP background, was built, checked against the diffuse X-ray
background, and retired the same day (D26).

## Milky Way halo — `source.halo`

NFW with $r_s = 20$ kpc, $\rho_\odot = 0.4$ GeV cm⁻³ at
$R_\odot = 8.1$ kpc; the cusp is softened inside 0.1 kpc so the exact
Galactic Centre ray stays finite. `column_density(l, b)` integrates
$D = \int\rho\,ds$ to 200 kpc with `scipy.integrate.quad`, one call
per ray (0.8 ms). Known answers: the anticentre ray has a closed form,
$D = \rho_s r_s\,[F(x_1) - F(x_0)]$ with $F(x) = \ln\frac{x}{1+x} +
\frac{1}{1+x}$, matched to $10^{-6}$; $D$ depends only on the angle
from the Centre direction.

| direction | $D$ / GeV cm⁻² |
|---|---:|
| Galactic Centre, boresight ray (cored) | $1.99\times10^{23}$ |
| 5° off the Centre | $1.10\times10^{23}$ |
| anticentre | $1.04\times10^{22}$ |

`sim.state_table` gains `d_gevcm2` (boresight), `d_fov_gevcm2` (cone
average) and `dk_fov_gevcm2_t2m2` $= \langle D\cdot K\rangle$, the
Milky Way line's figure of merit up to $\Theta$.

**Result, reference scenario (GC pointing in umbra):** the cone-averaged
$D$ is **0.64** of the boresight value — the 20° aperture averages
over the cusp, so a boresight $D$ overstates the line signal by half.
And $\langle D\cdot K\rangle / (\langle D\rangle\langle K\rangle) =
0.995$: the halo gradient and the field gradient across the cone are
uncorrelated, so the two averages may be taken separately to 0.5 %.
Both pinned in `test_scenario_regression`.

Caveat: the centre ray carries one third of the cone weight, so the
cone average of a cuspy $D$ is only as good as the core radius. The
ring-refinement check (ALP-CH-16) should be run for $D$ before the
Milky Way line is used for a number.

## Cosmic ALP background — checked and retired

**Model.** Conlon & Marsh 2013 (arXiv:1304.1804) eq. 5.18, the
matter-domination form $dn/dE \propto E^{1/2}\exp[-(E/E_*)^{3/2}]$, is
a Weibull distribution with shape 3/2; `scipy.stats.weibull_min` gave
the spectrum and band fraction. Mean energy 238 eV for a
$5\times10^6$ GeV modulus (eq. 5.13), scaling as $m_\Phi^{-1/2}$. Flux
$0.96\times10^6$ cm⁻² s⁻¹ at $\Delta N_{\rm eff} = 0.57$ (fig. 8),
linear in $\Delta N_{\rm eff}$.

**Why it could be checked early.** It is the only source in the study
with an absolute flux — set by $\Delta N_{\rm eff}$, not by an unknown
lifetime — so its converted brightness is a number at any coupling.

**Check.** Coherent conversion $P = (g\,B_\perp L/2)^2$ with
1 T = 195.35 eV², at the CAST limit $g = 6.6\times10^{-11}$ GeV⁻¹.
Converted in-band intensity (flux × band fraction / 4π × $P$) against
the CXB, $\int_1^{10} 11.6\,E^{-1.41}\,dE$ ph cm⁻² s⁻¹ sr⁻¹:

| $B_\perp L$ | $P$ | $\langle E\rangle$ | in band | converted / CXB |
|---:|---:|---:|---:|---:|
| 75 T m (reference median) | $6.0\times10^{-18}$ | 238 eV | $6.2\times10^{-4}$ | $1.6\times10^{-17}$ |
| 75 T m | $6.0\times10^{-18}$ | 532 eV | 0.11 | $2.9\times10^{-15}$ |
| 150 T m (reference max) | $2.4\times10^{-17}$ | 238 eV | $6.2\times10^{-4}$ | $6.6\times10^{-17}$ |
| 150 T m | $2.4\times10^{-17}$ | 532 eV | 0.11 | $1.2\times10^{-14}$ |

**Disposition.** Best case $10^{-14}$ of the background. ALP-CH-18 to
22 retired, `source/cab.py` removed (the model is in this branch's git
history). The band fraction D25 expected to decide it varies by 10³;
the conversion probability, at $10^{-17}$, is what decides it.

**What it tells the rest of the study.** The extragalactic
$\chi\to aa$ continuum converts through the same kernel at the same
$P$. To reach the diffuse background it needs an in-band ALP flux
about $10^{14}$ times the cosmic ALP background's. That is the
quantity the viability gate (D16) has to find in the allowed
parameter space.

## Links

- part of [[ALP]]
- requirements: [[04-plan/alp-baseline-requirements]] CH-05; CH-18 to 22 retired
- kernel over the aperture: [[2026-09-23-fov-field-integral]]
- decisions: [[decisions]] D15, D25, D26
