---
type: result
tags: [darkness, alp, source, nfw, cab, signal]
created: 2026-09-23
updated: 2026-09-23
status: active
---

# 2026-09-23 — the two source models: halo column and cosmic ALP background

New topic `source/`. With the conversion kernel already in `geometry/`,
all three ALP signal models in [[02-mission-analysis/conops-physics-map]]
now have their direction-dependent part in the library.

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

## Cosmic ALP background — `source.cab`

Conlon & Marsh 2013 (arXiv:1304.1804) eq. 5.18, the matter-domination
form: $dn/dE \propto E^{1/2}\exp[-(E/E_*)^{3/2}]$. That is a Weibull
distribution with shape 3/2, so `scipy.stats.weibull_min` supplies the
pdf, the cdf and the mean $\langle E\rangle = E_*\,\Gamma(5/3)$ with no
numerics of ours. The mean energy is the declared parameter (ALP-CH-19);
the paper's worked example gives 238 eV for a $5\times10^6$ GeV modulus
and scales as $m_\Phi^{-1/2}$. Flux $0.96\times10^6$ cm⁻² s⁻¹ at
$\Delta N_{\rm eff} = 0.57$, linear in $\Delta N_{\rm eff}$.

**ALP-CH-21, in-band fraction (1–10 keV):**

| $m_\Phi$ / GeV | $\langle E\rangle$ | fraction in band | in-band flux / cm⁻² s⁻¹ |
|---:|---:|---:|---:|
| $5\times10^6$ | 238 eV | $6.2\times10^{-4}$ | 600 |
| $10^6$ | 532 eV | 0.11 | $1.1\times10^{5}$ |

So whether the CAB tail matters is a modulus-mass question: three
orders of magnitude between the two ends of the motivated range. The
requirement is met as an analysis; the disposition (D25, retire or
keep) waits on the viability gate, where this flux is compared with
the $\chi\to aa$ benchmark.

## Links

- part of [[ALP]]
- requirements: [[04-plan/alp-baseline-requirements]] CH-05, CH-18, CH-19, CH-21
- kernel over the aperture: [[2026-09-23-fov-field-integral]]
- decisions: [[decisions]] D15, D25
