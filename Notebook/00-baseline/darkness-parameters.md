---
type: note
tags: [darkness, alp, baseline, parameters]
created: 2026-07-28
updated: 2026-09-08
status: active
---

# DarkNESS parameter register

Canonical numbers for the DarkNESS ALP study. **Every parameter used anywhere in this line of work
resolves to a row in this table.** If a number is not here, it is not yet real.

## Provenance tags

| Tag | Meaning |
|---|---|
| `DN-V` | DarkNESS, **verified** against Alpine et al. 2025 (ASR 76, 4793) with page number |
| `DN-TBC` | DarkNESS-specific but **not yet confirmed** — needs the team, a design doc, or an ICD |
| `EXT` | External literature (Yamamoto 2020, IGRF, etc.) |
| `ASSUME` | Our modelling choice, made here, revisable |
| `DERIV` | Derived in this vault, with the derivation shown |

The discipline: never let a `DN-TBC` or `ASSUME` silently become a `DN-V`. A projected sensitivity
curve inherits the weakest tag in its chain.

## Instrument

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Sensors | 4 × skipper-CCD, 1.35 Mpix each | `DN-V` | p. 4797, Fig. 3 |
| Pixel pitch | 15 × 15 µm | `DN-V` | p. 4798 |
| Total collecting area | **12 cm²** | `DN-V` | p. 4797 |
| Depletion thickness | 725 µm, fully depleted | `DN-V` | p. 4796 |
| Entrance window | 50 nm Al, >98 % transmission down to 1 keV | `DN-V` | p. 4796 |
| Science band | 1–10 keV | `DN-V` | p. 4794, 4796 |
| Energy resolution | σ_E ≈ 50 eV at 6 keV (Fano limit in Si) | `DN-V` | p. 4798 |
| Resolution goal | Fano-limited across 1–10 keV, <1 min readout | `DN-V` | p. 4798 |
| Readout | 250 kPix/s per skipper sample; full frame in 5 s | `DN-V` | p. 4796 |
| Operating temperature | 170 ± 5 K | `DN-V` | p. 4796, 4800 |
| Optics | **None** (volume-constrained) | `DN-V` | p. 4797 |
| Field of view | 20°, set by four circular apertures | `DN-V` | p. 4797 |
| FOV convention | 20° = **full cone** → half-angle 10°, Ω ≈ 0.0955 sr | `DERIV` | see below |
| Masking live fraction | ~50 % (high-energy hit masking) | `DN-V` | p. 4795, 4798 |
| Aperture body axis | unknown — Fig. 8 labels the window but the axis is ambiguous | `DN-TBC` | p. 4800 |

### Two corrections to earlier working numbers

- The `LimitCalculation` sterile-neutrino chain uses `area_cm2 = 8.0` and `efficiency = 0.20`. The paper
  states **12 cm²**. Whatever 8 cm² represented (a de-rating? an earlier design?) it is not the published
  collecting area — resolve before reusing that chain. See [[../open-questions|open questions]].
- Cross-check on 12 cm²: 4 × 1.35×10⁶ px × (15 µm)² = **12.15 cm²** `DERIV`. The published figure is the
  raw sensor area, so effective area is 12 cm² × QE(E) × live fraction.

### Why 20° is read as a full cone

The paper states one DarkNESS exposure sees diffuse flux "comparable to 22 XMM EPIC-MOS images" (p. 4797),
with EPIC-MOS at 30 arcmin FOV and 700 cm² at 3 keV. That gives an MOS grasp of

$$
A\,\Omega\big|_{\rm MOS} = 700\ {\rm cm^2} \times 5.98\times10^{-5}\ {\rm sr} = 4.19\times10^{-2}\ {\rm cm^2\,sr}
$$

so 22 × MOS ≈ 0.92 cm² sr. With A = 12 cm² that implies Ω ≈ 0.077 sr, i.e. a half-angle of ≈ 9°.
A 10° half-angle (Ω = 0.0955 sr) gives 27 × MOS — consistent within the slop of which energy and QE are
assumed. A 20° **half**-angle would give 108 ×, which is not what the paper claims.

**So: half-angle 10°, Ω ≈ 0.0955 sr.** Tagged `DERIV` and not `DN-V` because §2.2 separately refers to a
"20° radius" region for the Galactic Centre *background model* — that is a sky region for background
estimation, not the FOV, but the collision of terms is exactly the kind of thing that needs confirming.

## Grasp, and what it buys

| Instrument | Effective area | Ω [sr] | Grasp [cm² sr] |
|---|---|---|---|
| DarkNESS, geometric | 12 cm² | 0.0955 | 1.15 |
| DarkNESS, with 50 % masking and QE ~0.9 | ~5.4 cm² | 0.0955 | ~0.52 |
| Suzaku XIS, one unit | ~330 cm² at 1.5 keV | 2.68×10⁻⁵ | 8.8×10⁻³ |
| Suzaku XIS, three units (Yamamoto's set) | — | — | 2.6×10⁻² |

`DERIV`, Suzaku numbers `EXT`. DarkNESS has roughly **20× the grasp** Yamamoto had, conservatively.
Because the signal is diffuse, this is the correct comparison — not effective area, where a focusing
telescope wins by two orders of magnitude. See [[../01-physics/sensitivity-scaling|sensitivity scaling]]
for what 20× actually buys (spoiler: 20^(1/4) ≈ 2.1 in coupling).

## Platform and operations

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Bus | NanoAvionics M6P, 6U | `DN-V` | p. 4799 |
| ADCS | Reaction wheels, IMU, magnetorquers | `DN-V` | p. 4800 |
| Attitude modes | Sun-Tracking, Ground Station Pass, Inertial Science Pointing | `DN-V` | p. 4800 |
| Pointing constraint structure | Primary axis (science) + secondary axis (radiators to deep space, away from Earth) | `DN-V` | p. 4800 |
| Launch baseline in 2025 paper | Firefly Alpha, Exolaunch NOVA dispenser, NET mid-2026 | `DN-V` | p. 4799; time-dependent and now requires mission-team refresh |
| Orbit | ~500 km SSO **or** ISS-like mid-inclination; set at manifest | `DN-V` | p. 4799 |
| Mission end | Natural decay within five years | `DN-V` | p. 4799 |
| Science phase in 2025 paper | 187 days, 2026-03-20 → 2026-09-23, umbral passages | `DN-V` | p. 4799; historical planning baseline, not current status |
| Planned GC exposure | 0.5 Ms in 2025 mission paper; 1 Ms in 2026 detector paper | `DN-TBC` | Alpine et al. 2025 p. 4795; Alpine et al. 2026 arXiv:2602.02461 |
| Slew rate / settle time | unknown | `DN-TBC` | — |
| Mass / power | 10.3 kg, 32.3 W avg, 37.6 W peak | `DN-V` | p. 4802, Table 1 |

## Environment

| Quantity | Value | Tag | Source |
|---|---|---|---|
| Trapped proton fluence at 450 km | 9×10⁸ cm⁻² yr⁻¹ at 10 MeV | `DN-V` | p. 4798 |
| Radiation-induced trap density | 8×10⁴ cm⁻² → 0.18 traps/pixel | `DN-V` | p. 4798 |
| Pixels acquiring traps | ~5 % per year in LEO | `DN-V` | p. 4798 |
| Cherenkov background | ~0.1 e⁻ px⁻¹ hr⁻¹, L2 estimate, LEO modelling ongoing | `DN-V` | p. 4795 |

## Links

- part of [[../ALP]]
- ConOps detail: [[darkness-conops]]
- what this feeds: [[../01-physics/alp-signal-chain]], [[../03-sensitivity/method]]
- unresolved: [[../open-questions]]
