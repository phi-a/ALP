# Yamamoto Four-Field Geometry Cohort

## Purpose

This work package extends the validated `101002010` calculation to the four
Suzaku fields used by Yamamoto: Lockman Hole, MBM16, SEP, and NEP. It is a
geometry-only reproduction using archived EHK state, cleaned XIS GTIs, FORMS,
IGRF-13, a 60-second cadence, coherent conversion at `q = 0`, and a line-of-sight
boundary of six Earth radii.

It does not calculate spectra, detector response, background, ALP limits,
DarkNESS orbit performance, or field-of-view averages.

## Observation Provenance

The primary manifest contains the 23 observations listed in Appendix A,
Table A.1 of Yamamoto's 2018 doctoral thesis:

- Lockman Hole: 9
- MBM16: 6
- SEP: 4
- NEP: 4

`104002020` is recorded as a supplemental Lockman observation and is excluded
from the primary aggregate. Yamamoto et al. state that 11 Lockman observations
were used, but the currently identified thesis and archive records do not
provide 11 unique primary IDs. The software records this discrepancy and does
not duplicate an ObsID to reproduce the stated count.

Sources:

- R. Yamamoto, *A Search for a Contribution from Axion-Like Particles to the
  X-Ray Diffuse Background Utilizing the Earth's Magnetic Field*, doctoral
  thesis (2018):
  https://www.isas.jaxa.jp/home/yamasaki/theses/Dthesis_2018_RYamamoto.pdf
- R. Yamamoto et al., JCAP 05 (2020) 011:
  https://arxiv.org/abs/1906.04429

## Notebook Workflow

Open `Main_Yamamoto_Cohort.ipynb` with the existing project virtual-environment
kernel. Its defaults perform a local readiness inspection only.

1. Run all cells with `ACQUIRE_MISSING = False` and `RUN_ANALYSIS = False`.
2. Review the 24 primary-plus-supplemental readiness rows.
3. Set `ACQUIRE_MISSING = True` to fetch missing EHK and all standard cleaned
   3x3/5x5 event/GTI products for the selected XIS detector. Their GTIs are
   merged as a union so overlapping observing modes are counted once.
4. Return `ACQUIRE_MISSING` to `False`, set `OBSERVATION_LIMIT = 1`, and set
   `RUN_ANALYSIS = True` for a smoke run.
5. Set `OBSERVATION_LIMIT = None` for the full cohort after product readiness is
   23/23.

`FORCE = False` reuses an observation only when its source hashes, FORMS
revision, analysis version, IGRF model, and numerical settings match.

## Outputs And Acceptance

Aggregate products are written under `outputs/yamamoto_cohort/`. Individual
state tables, figures, summaries, and provenance remain under
`outputs/yamamoto_<ObsID>/`.

The cohort package includes:

- provenance-bearing manifest CSV and JSON;
- observation and field summaries with exposure-weighted quantiles;
- published-bin occupancy and mean comparison;
- normalized four-field exposure distributions;
- missing, invalid, mismatched, and failed-observation records.

The cohort passes only when all 23 primary observations are ready, every
observation has a valid integral fraction of 1.0 and convergence of at least
99%, each merged GTI exposure agrees with the thesis to within 0.1 ks, and every
published bin is populated with a calculated mean within 15% of the thesis
value. A failure is reported as a discrepancy; calculation settings and
membership are not tuned automatically.
