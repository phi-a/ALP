---
type: note
tags: [darkness, alp, detector, skipper-ccd, parameters]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Skipper-CCD detector sheet

Every detector property the ALP channel needs, in one place, with where
it enters the count model. Provenance tags as in
[[darkness-parameters]], plus one more:

| Tag | Meaning |
|---|---|
| `DN-D` | DarkNESS X-ray sensors paper, **internal draft** (Alpine et al., JINST, in prep.; `docs/DarkNESS_Xraysensors.pdf`). Still has reviewer notes in the text; confirm before quoting |

"ASR" below is Alpine et al. 2025, ASR 76, 4793
(`docs/ASR2025-DarkNESS-publish.pdf`), cited by page.

## Where each number enters

The signal expectation from
[[../01-physics/detection-channel-derivation-contract]] §3 is

$$
\mu^{\rm sig}_{ij}=\int_{\Delta t_i}dt\int d\Omega\int dE\;
I_a P_{a\to\gamma}\,
A_{\rm geo}\,\mathcal{V}(\theta)\,
T_{\rm Al}(E)\,\eta_{\rm Si}(E)\,
\epsilon_{\rm sel}\,f_{\rm live}\,R_j(E).
$$

| Symbol | Detector property | Section below |
|---|---|---|
| $A_{\rm geo}$ | sensor area facing the sky | Geometry |
| $\mathcal V(\theta)$, $\int d\Omega$ | aperture acceptance vs off-axis angle | Field of view |
| $T_{\rm Al}\,\eta_{\rm Si}$ | window transmission × absorption in silicon (QE) | Quantum efficiency |
| $R_j(E)$ | energy redistribution: gain, resolution, tails | Energy response |
| $\epsilon_{\rm sel}$ | event-grade and cluster cuts | Event selection |
| $f_{\rm live}$ | masking and readout dead time | Event selection |
| $\Delta t_i$ | exposure and spectrum cadence | Time structure |

The background side ($Z\beta$) uses the same response plus the
particle-induced terms under Backgrounds.

## Geometry

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Sensors | 4 skipper-CCDs on one ceramic multi-chip module (MCM) | `DN-V` | ASR p. 4796 |
| Format per sensor | 1058 × 1278 px (1.35 Mpix) | `DN-D` | Table 1 (Oscura prototype; flight format assumed equal) |
| Pixel pitch | 15 µm | `DN-V` | ASR p. 4798 |
| Area per sensor | 3.04 cm² | `DERIV` | 1058 × 1278 × (15 µm)² |
| Total geometric area $A_{\rm geo}$ | 12 cm² (12.17 derived) | `DN-V` | ASR p. 4797 |
| Amplifiers | 4 per sensor, one per quadrant (16 total) | `DN-D` | §3 |
| Optics | none; aperture-defined | `DN-V` | ASR p. 4797 |

Gain differs 12–16 % between quadrants (`DN-D`, §5.1), so each of the 16
quadrants needs its own calibration; treat them as 16 sub-detectors
with a shared sky.

## Field of view

The FOV is **fixed** to the body: four circular apertures in front of
the array set it (ASR p. 4797). What the mission sets is where the
boresight points, not the FOV size.

| Quantity | Value | Tag | Source |
|---|---|---|---|
| FOV per pixel | **20° full cone** → half-angle 10°, Ω = 0.0955 sr | `DN-V` | ASR p. 4797; confirmed by the team 2026-09-24 |
| Grasp | $A_{\rm geo}\Omega$ = 12 × 0.0955 = **1.15 cm² sr** | `DERIV` | matches ASR "22 × EPIC-MOS" (27×) |
| Keep-out cone | 40°, the union of the 20° pixel cones across the array plus margin; for Earth/Moon obstruction, not acceptance | `DN-V` | ASR p. 4801–4802, Fig. 10 |
| Pointing error | 4.5° absolute, 1.5° knowledge (3σ) | `DN-V` | ASR p. 4801 |

The sensors draft quotes **4.6 cm² sr** (§5.2). That is 12 cm² over a
20° *half*-angle cone (0.379 sr), so it double-counts the FOV. The value
consistent with a 20° FOV is 1.15 cm² sr; the draft should be corrected.

Each pixel sees its own 20° cone, offset by its position behind the
apertures, so the array as a whole sees further than any one pixel. That
is why obstruction checks use 40° while the per-pixel acceptance is 20°.

Also unknown: the angular response $\mathcal V(\theta)$. A flat top out
to the edge is an upper bound. Circular apertures over a 2 × 2 array
give a response that falls off with angle and differs from pixel to
pixel (edge pixels see further, ASR p. 4801). The grasp that matters
is $A_{\rm geo}\int\mathcal V\,d\Omega$, not $A_{\rm geo}\,\Omega_{\rm edge}$.

## Quantum efficiency

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Science band | 1–10 keV | `DN-V` | ASR p. 4794 |
| Entrance window | 50 nm Al; >98 % X-ray transmission down to 1 keV | `DN-V` | ASR p. 4796 |
| Si thickness, prototype | 725 µm, fully depleted | `DN-V` | ASR p. 4796 |
| Si thickness, **flight** | **500 µm** (thinned to cut particle tracks) | `DN-D` | §2, Table 1 |
| Absorption at 10 keV | 99.6 % (725 µm), 97.6 % (500 µm) | `DERIV` | Si attenuation length ≈ 134 µm at 10 keV |
| Active mass | 2.0 g (725 µm) → 1.4 g (500 µm) | `DERIV` | ASR quotes ≈ 2 g, p. 4794 |
| Front-side dead layer | not published | `DN-TBC` | sets QE below ~2 keV |

The register still says 725 µm; the flight value is 500 µm. For the
ALP band the change is small (≤ 2.5 % at 10 keV) but it cuts the
particle background per pixel, which matters more.

## Energy response

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Fano limit | σ_E ≈ 50 eV at 6 keV (FWHM ≈ 120 eV) | `DN-V` | ASR p. 4798 |
| Fano formula | $\sigma_E=\sqrt{F\,w\,E}$, F ≈ 0.12, w ≈ 3.7 eV/e⁻ | `EXT` | Rodrigues et al. 2021 |
| Measured, unirradiated (NI2) | **169 ± 1 eV FWHM** at 5.9 keV | `DN-D` | Table 2 |
| Measured, adjacent (IA2) | 197 ± 2 eV FWHM | `DN-D` | Table 2 |
| Measured, irradiated (BI4) | 352 ± 9 eV FWHM, low-energy tail | `DN-D` | Table 2 |
| Pixel noise used | 3.5–3.8 e⁻ (10 skipper samples) | `DN-D` | §4.2–4.3 |
| Single-sample noise | < 4 e⁻ RMS | `DN-D` | Table 1 |
| Deep-sample noise | 0.2 e⁻ at 300 samples | `DN-V` | ASR Fig. 4 |
| Goal | Fano-limited over 1–10 keV with < 1 min readout | `DN-V` | ASR p. 4798 |
| End of life, linear model | 173–198 eV FWHM (ISS 1 yr → SSO 3 yr) | `DN-D` | Table 4 |
| End of life, quadrature model | 169–172 eV FWHM | `DN-D` | Table 4 |
| Damage coefficient | ΔFWHM/DDD ≈ 1.1 × 10⁻⁶ eV per MeV g⁻¹ | `DN-D` | Eq. 5.1 |

Budget at 5.9 keV: 169 eV measured vs 120 eV Fano leaves ≈ 119 eV FWHM
of readout noise summed over the cluster pixels. More skipper samples
shrink it as $1/\sqrt{N}$ but cost readout time. The flight sample
count is `DN-TBC`.

For the ALP search resolution matters less than for a line search. The
extragalactic ALP signal is a continuum below $E_0$, and the
geomagnetic signal is identified by its time modulation, not a narrow
feature. Resolution sets the bin width $R_j$ and how much background
sits in each bin. The Milky Way line component is where it bites.

## Event selection and live time

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Clustering | seed 9σ, split 3σ, 4-neighbour | `DN-D` | §4.3 |
| Kept grades | single, 2-split, L-split | `DN-D` | §5.1 |
| Grade retention (irradiated vs clean) | 26 % vs NI2, 38 % vs IA2 | `DN-D` | §5.1; definition still loose in draft |
| Compact events per image, 100-row | NI2 155, IA2 109, BI4 41 | `DERIV` | Table 3 |
| Masking live fraction | ≈ 50 % after masking high-energy hits | `DN-V` | ASR p. 4795, 4798 |
| CTI, 1 yr LEO | ~5 % of pixels gain traps per year | `DN-V` | ASR p. 4798 |
| CTI, lab | 115 (clean), 242 (adjacent), 695 (irradiated) ppm px⁻¹ | `DN-D` | §5.1 |

$\epsilon_{\rm sel}$ drifts down with radiation age and $f_{\rm live}$
depends on the particle rate, which tracks the geomagnetic cutoff —
the same variable that drives the ALP kernel. Both belong in the
nuisance design matrix, not as fixed constants.

## Operating point

| Quantity | Flight | Lab (draft) | Tag |
|---|---|---|---|
| Temperature | 170 ± 5 K (Ricor K508N cryocooler) | 153 K | `DN-V` / `DN-D` |
| Back bias | 40 V | 70 V | `DN-D` |
| Readout speed | 250 kpix/s per skipper sample; full frame 5 s | — | `DN-V` |
| Electronics | sLTA, 10 W | LTA | `DN-V` |

## Time structure

| Quantity | Value | Tag | Source |
|---|---|---|---|
| GC observation | 15 min, umbra only, splittable into shorter frames | `DN-V` | ASR p. 4795 |
| Planned GC observations | 600 (≈ 150 h ≈ 0.5 Ms) | `DN-V` | ASR Table 2, p. 4803 |
| Exposure target | 1 Ms | `DN-D` | §1, §5.2 |
| Downlinked product | one histogram per observation (2.5 kB); raw frames (32 MB) for 10 % | `DN-V` | ASR p. 4801, Table 3 |

The shortest ALP time bin is set by the downlinked histogram, i.e. one
spectrum per observation, unless raw frames are pulled. That is the
$\Delta t_i$ in the count model.

## Backgrounds set by the detector

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Cherenkov (L2 estimate) | ~0.1 e⁻ px⁻¹ h⁻¹; masking cuts it ~10× | `DN-V` | ASR p. 4795 |
| Trapped-proton fluence, 450 km | 9 × 10⁸ cm⁻² yr⁻¹ at 10 MeV | `DN-V` | ASR p. 4798 |
| 3-yr proton fluence (95th pct) | 3.9 × 10⁹ (ISS), 8.7 × 10⁹ (SSO) cm⁻² | `DN-D` | Table 4 |
| Dark current | suppressed by 170 K; value not published | `DN-TBC` | ASR p. 4797 |
| Particle (NXB) spectrum in 1–10 keV | not published; proxy in `background` | `ASSUME` | [[../03-sensitivity/method]] |

## Open detector questions

- FOV half-angle 10° or 20°, and the shape of $\mathcal V(\theta)$ (Q1).
- Flight skipper sample count, hence flight noise and resolution.
- Front-side dead layer, hence QE at 1–2 keV.
- Flight frame length inside a 15-min observation.
- Whether per-frame time tags survive in the downlinked histogram.
- In-orbit NXB spectrum per pixel and its cutoff-rigidity dependence
  (Q7).

## Links

- part of [[../ALP]]
- register: [[darkness-parameters]]
- count model: [[../01-physics/detection-channel-derivation-contract]]
- unresolved: [[../open-questions]]
