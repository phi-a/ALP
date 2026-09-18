---
type: validation-record
tags: [darkness, alp, yamamoto, suzaku, forms]
created: 2026-07-31
updated: 2026-07-31
status: archived
---

# Yamamoto four-field geometry validation

> **Archival record, 2026-09-17.** The code behind this result
> (`src/darknessalp/yamamoto/`, the Suzaku archive loader, and the
> notebooks that drove them) was removed when the library was rebuilt;
> it is recoverable from git history. The result stands as the
> provenance for decision D9. The current kernel is validated instead by
> a data-free Suzaku-like gate — see [[testing]] §4 — which reproduces
> Yamamoto's reported $(B_\perp L)^2$ band without the archive.

## Gate result

The Suzaku geometry cohort is the accepted validation gate for the
DarkNESS ALP line-of-sight kernel.

| Quantity | Result |
|---|---:|
| Primary observations | 23 / 23 ready and accepted |
| Fields | Lockman Hole, MBM16, SEP, NEP |
| GTI exposure agreement | every observation within 0.1 ks of thesis |
| Valid field-integral fraction | 100% per observation |
| Numerical convergence | 100% per observation |
| Published bins within 15% | all |
| Largest bin-mean difference | 2.76% |
| Field model | FORMS IGRF-13 |
| Cadence | 60 s |
| Integration boundary | 6 Earth radii |

## Important ingestion correction

Suzaku observations can contain multiple standard cleaned XIS event products
for 3x3 and 5x5 modes. Selecting one file can discard most of an observation.
The production ingestion now:

1. selects one detector using XIS0, XIS1, XIS3 precedence;
2. includes every standard 3x3 and 5x5 cleaned product for that detector;
3. excludes timing-mode products;
4. merges the GTIs as a union so overlaps are counted once; and
5. verifies the resulting exposure against the thesis table.

For example, Lockman observation `108001010` changed from an incorrect 8.4 s
to 38.852 ks, consistent with the published 38.8 ks.

## Provenance

- Code: `C:\Users\phial\Documents\Python\darkmatter\ALP`
- Notebook: `Main_Yamamoto_Cohort.ipynb`
- Aggregate output: `outputs\yamamoto_cohort\cohort_summary.json`
- State tables: `outputs\yamamoto_<ObsID>\frame_state.csv`
- `darkness_alp` version: 0.2.0
- FORMS revision: `f6d320234e38abf781bdb372427c4e8ec899050a`

The published-bin means are a useful consistency check but are partly
constrained by the bin edges themselves. The exposure reconstruction,
frame/field cross-checks, numerical convergence, and full field distributions
are the stronger validation evidence.

## Consequence

The validated kernel may now be applied to a FORMS-propagated DarkNESS state
table. Spectral backgrounds, detector response, coupling limits, and pointing
optimization remain outside this validation record.

## Links

- [[yamamoto-validation-101002010]] - historical first vertical slice
- [[geomagnetic-integral]]
- [[../04-plan/next-step]]
- [[../decisions]]
