---
title: Yamamoto Geometry Validation - Suzaku 101002010
status: archived
updated: 2026-07-30
---

# Yamamoto Geometry Validation - Suzaku 101002010

> **Archival record, 2026-09-17.** The code behind this result
> (`src/darknessalp/yamamoto/`, the Suzaku archive loader, and the
> notebooks that drove them) was removed when the library was rebuilt;
> it is recoverable from git history. The result stands as the
> provenance for decision D9. The current kernel is validated instead by
> a data-free Suzaku-like gate — see [[testing]] §4 — which reproduces
> Yamamoto's reported $(B_\perp L)^2$ band without the archive.

## Result

The first archived-state vertical slice passes its defined geometry,
convergence, and FORMS-integration gates.

The calculation used the cleaned XIS0 GTIs, 60-second exposure-centered
samples, EHK spacecraft position and pointing, FORMS frame transformations,
FORMS IGRF-13, and a vector line-of-sight integral from Suzaku to a spherical
boundary at 6 Earth radii.

| Quantity | Result |
|---|---:|
| Cleaned-GTI exposure | 59,001.07 s |
| State-table samples | 999 |
| Valid field integrals | 999 |
| Numerically converged | 999 |
| Raw median $(B_\perp L)^2$ | 16,405.83 T2 m2 |
| Raw 5th-95th percentile | 2,501.98-49,296.17 T2 m2 |
| Raw maximum | 62,364.35 T2 m2 |
| Yamamoto-screened samples | 698 |
| Yamamoto-screened exposure | 41,298.71 s |
| Screened median $(B_\perp L)^2$ | 15,701.51 T2 m2 |
| FORMS `BGCRS` cross-check | exact for the checked sample |

The median and upper distribution reproduce Yamamoto's stated typical
$10^4$-$10^5$ T2 m2 scale. Values below $10^4$ T2 m2 are present and are not
removed or tuned away.

## Screening

The cleaned event GTIs are retained as the base exposure. A separate
Yamamoto-like screening flag requires:

```text
SAA == 0
COR2 >= 8 GV
ELV >= 5 deg
DYE_ELV >= 20 deg
```

The state table retains all raw covariates and flags. In the base GTIs, 300
samples have `COR2 < 8 GV` and eight have a nonzero `SAA` flag. This confirms
that the paper's extra selection cannot be inferred from the cleaned event GTIs
alone and must remain explicit.

## Reproduction

From the repository root:

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m darkness_alp.validate_yamamoto --obsid 101002010
```

Artifacts are under `outputs/yamamoto_101002010/`:

- `frame_state.csv`: time-indexed mission state and conversion regressor;
- `summary.json`: distributions, quality counts, and gate decision;
- `provenance.json`: units, source hashes, FORMS revision, and model settings;
- `field_integral_time.png`: orbital time dependence and GTI gaps;
- `field_integral_histogram.png`: regressor distribution;
- `field_integral_covariates.png`: first identifiability diagnostics.

## Interpretation and limits

This result establishes that the archived state, frame chain, IGRF field, ray
geometry, units, and vector integration produce the expected scale for one
Lockman Hole observation. It is sufficient to begin the next mission-analysis
stage, but it is not yet a reproduction of the Yamamoto paper or Figure 7.

Remaining validation work:

1. Repeat the calculation over all Yamamoto observations and compare the four
   field distributions with the published Figure 2 exposure histograms.
2. Add selectable IGRF-12 support in FORMS and quantify the model-version
   difference relative to the IGRF-13 baseline.
3. Confirm the exact Suzaku screening expression and detector combination used
   for each field.
4. Reproduce the ALP spectral normalization and likelihood before projecting a
   DarkNESS coupling limit.

The next engineering work may proceed in parallel with items 1-3: create the
FORMS DarkNESS routine and generate a representative orbit state table using
the same schema. The spectral-background simulator and Figure 7 projection
remain deferred.
