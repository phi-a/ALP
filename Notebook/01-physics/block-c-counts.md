---
type: derivation
tags: [darkness, alp, physics, derivation, detector, counts, block-c]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Block C — from photon intensity to skipper-CCD counts

This note takes the converted-photon intensity from Blocks A and B to
the expected counts per time sample and energy bin, with every
detector factor separate and its number from
[[../00-baseline/skipper-ccd]], and checks the count integral against
the contract's conditions. Keys refer to [[../references]].

## Result

For time sample $i$ of length $\Delta t_i$ with aperture-averaged
kernel $K_i$, and energy bin $j$:

$$
\mu_{ij} = \Delta t_i\;\left(\frac g2\right)^2 K_i\;
A_{\rm geo}\,\Omega\;f_{\rm live}\,\epsilon_{\rm sel}
\int dE\;\frac{dI}{dE}(E)\;{\rm QE}(E)\;R_j(E),
$$

$$
{\rm QE}(E) = e^{-\mu_{\rm Al}(E)\,d_{\rm Al}}\,
e^{-\mu_{\rm Si}(E)\,d_{\rm dead}}\,
\big(1 - e^{-\mu_{\rm Si}(E)\,d_{\rm Si}}\big),
\qquad
R_j(E) = \Phi\!\Big(\tfrac{E_{j+1} - E}{\sigma(E)}\Big)
 - \Phi\!\Big(\tfrac{E_j - E}{\sigma(E)}\Big),
$$

$$
\sigma(E) = \frac{{\rm FWHM}(E)}{2\sqrt{2\ln2}},\qquad
{\rm FWHM}^2 = \big(2\sqrt{2\ln2}\big)^2 F\,w\,E + {\rm FWHM}_{\rm noise}^2 .
$$

The Milky Way line at $E_0$ is the same integral with
$dI/dE = I_{\rm line}\,\delta(E - E_0)$ and $K_i$ replaced by the
aperture average of $D\cdot K$ divided by $D$, i.e. the state table's
`dk_fov_gevcm2_t2m2` carries $\langle D K\rangle_i$ directly.

Code: `detector.quantum_efficiency`, `detector.resolution_fwhm_kev`,
`detector.redistribution`, `detector.grasp_cm2sr`,
`detector.expected_counts`; inputs `source.line_intensity`,
`source.continuum_intensity`, `geometry.conversion_probability`.

## 1. The chain of factors

Photons arriving from direction $\hat n$ at energy $E$ in the interval
$dt$ number $I_\gamma(E,\hat n,t)\,dE\,d\Omega\,dt$ per unit area,
with $I_\gamma = I_a P_{a\to\gamma}$. Each factor below is a separate
fraction of them, applied once.

| Factor | What it is | Value | Basis |
|---|---|---|---|
| $A_{\rm geo}$ | sensor area facing the sky | 12 cm² | `[Alp25]` |
| $\Omega$ | aperture cone, flat response to 10° | 0.0955 sr | `[Alp25]`, team; $\mathcal V(\theta)$ open |
| $P$ | conversion, direction- and time-dependent | $(g/2)^2 K$ | Block A |
| $T_{\rm Al}$ | 50 nm Al window | 0.984 at 1 keV, 0.951 at 1.6 keV (K edge), > 0.99 above 3 keV | NIST µ/ρ |
| $\eta_{\rm Si}$ | 500 µm fully depleted Si | 0.981 at 10 keV; ≈ 1 below 5 keV | NIST µ/ρ |
| $d_{\rm dead}$ | front-side inactive Si | 0 (open) | `DN-TBC` |
| $f_{\rm live}$ | pixels left after masking | 0.5 | `[Alp25]` |
| $\epsilon_{\rm sel}$ | event-grade retention | 1 now; falls with dose | `[Alp26]`, open |
| $R_j$ | Gaussian redistribution | 169 eV FWHM at 5.9 keV; 198 eV end of life (SSO, 3 yr) | `[Alp26]` |

The Fano term uses $F = 0.118$, $w = 3.72$ eV; the noise term 119 eV
FWHM is what remains of the measured 169 eV after the 120 eV Fano
width is removed in quadrature, and stands in for the unknown flight
skipper-sample count.

$f_{\rm live}$ and $\epsilon_{\rm sel}$ vary with the particle rate,
which follows the same geomagnetic position as $K$. In the likelihood
they are nuisance terms with their own time dependence, not constants;
here they enter as scalars so the count model stays separable.

## 2. Aperture average

$P$ varies across the 20° cone. The count integral over $d\Omega$ is
the cone average $\langle K\rangle_i$ from the 19-ray quadrature times
$\Omega$, which is what the state table stores
([[../2026-09-23-fov-field-integral]]). For the line the source also
varies across the cone, so the average is of the product
$\langle D K\rangle_i$; on the reference day it equals
$\langle D\rangle\langle K\rangle$ to 0.5 %
([[../2026-09-23-source-models]]).

## 3. Worked example: the reference day

Reference schedule (420 km, 51.6°, Galactic Centre in umbra,
10-min cadence; 39 science samples, 6.5 h) with the D28 benchmark
$g = 5.8\times10^{-11}$ GeV⁻¹, $f/\tau = 6.3\times10^{-3}$ Gyr⁻¹,
$m_\chi = 7$ keV, $f_{\rm live} = 0.5$, $\epsilon_{\rm sel} = 1$:

| | per day | × 187 days | D28 (187-day run) |
|---|---|---|---|
| $\sum_i \Delta t_i \langle K\rangle_i$ | $1.95\times10^8$ T² m² s | | |
| $\sum_i \Delta t_i \langle DK\rangle_i$ | $2.47\times10^{31}$ GeV cm⁻² T² m² s | | |
| Milky Way line | $5.3\times10^{-5}$ | $9.8\times10^{-3}$ | $9\times10^{-3}$ |
| continuum, 1–10 keV | $5.6\times10^{-6}$ | $1.0\times10^{-3}$ | $1.2\times10^{-3}$ |

D28 used a throughput of 0.20 and 5.7 Ms of simulated exposure; this
chain uses $0.5\times{\rm QE}$ and 187 copies of one day (4.4 Ms).
With those conventions aligned the line counts agree to 5 % and the
continuum reflects the 2.1× correction of Block B. Forty percent of
the continuum counts fall in 1–2 keV, where the dead layer and the
Al edge are least known.

## 4. Checks

| # | Check | Test | Result |
|---|---|---|---|
| 1 | Constant-brightness sky, all efficiencies 1: counts $= I\,A\Omega\,\Delta E\,\Delta t$ | `test_constant_sky_recovers_the_grasp` | $10^{-9}$ |
| 2 | $\sum_j R_j(E) = 1$ | `test_redistribution_conserves_counts` | $10^{-9}$ |
| 3 | A narrow line keeps its total through $R_j$ and spreads more at 198 eV than at 169 eV | `test_monochromatic_line_is_conserved_and_widened_by_age` | conserved to $10^{-9}$; peak bin lower |
| 4 | $f_{\rm live}$ and $\epsilon_{\rm sel}$ enter once, linearly | `test_losses_enter_once_and_linearly` | 0.4 for 0.5 × 0.8 |
| 5 | Samples scale with $P_i\Delta t_i$ | `test_samples_scale_with_probability_and_time` | yes |
| 6 | Cone average tends to the boresight as the half-angle → 0 | `test_fov_hairline_cone_is_the_boresight` (ALP-CH-17) | $10^{-6}$ |
| 7 | Window > 98 % at 1 keV (`[Alp25]`) | `test_window_matches_the_asr_statement` | 98.4 % |
| 8 | Si absorption from NIST: 98.1 % (500 µm), 99.7 % (725 µm) at 10 keV | `test_silicon_from_nist_attenuation` | yes |
| 9 | Resolution model returns the measured 169 eV at Mn Kα; Fano alone 120 eV | `test_resolution_reproduces_the_measured_width` | yes |
| 10 | K edges: Al edge visible; Si edge visible only through a dead layer | `test_edges_and_dead_layer` | yes |

In `tests/test_detector.py` and `tests/test_geometry_los.py`.

## Close

The count model is the product of separately stated factors, each
applied once, with the redistribution conserving counts and the grasp
recovered exactly for a uniform sky. Run on the reference day it
reproduces D28's line count within the stated conventions. What is
not derived but declared: the flat angular response
$\mathcal V(\theta)$, the dead layer (both bite at 1–2 keV, where 40 %
of the continuum lies), and $\epsilon_{\rm sel}$, which with
$f_{\rm live}$ must become time-dependent nuisance terms in Block D.

## Links

- contract §3: [[detection-channel-derivation-contract]]
- detector sheet: [[../00-baseline/skipper-ccd]]
- next: Block D, likelihood and the identifiable claim
