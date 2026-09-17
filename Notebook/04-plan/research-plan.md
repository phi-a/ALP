---
type: plan
tags: [darkness, alp, plan]
created: 2026-07-28
updated: 2026-09-08
status: active
---

# Research plan

The [[project-charter]] defines the question and publication boundary. The
current committed analysis is [[next-step]].

## Result sequence

The project proceeds through six dependent results.

1. The source and detection derivation defines the measurable parameter and
   tests whether any allowed benchmark is within reach.
2. The Suzaku reconstruction validates the geomagnetic conversion kernel and
   its count normalization.
3. The DarkNESS mission-state analysis defines the accessible conversion
   geometries under the adopted operations constraints.
4. The identifiability analysis determines whether conversion variation
   survives the fitted background covariates.
5. The joint-source analysis measures the Milky Way and extragalactic
   information contributions under one shared decay normalization.
6. The detector and likelihood calculation translates the measurement into a
   source-normalized sensitivity and conditional coupling curve.

The first five results form the minimum SmallSat 2027 reach or no-reach paper.
The final result completes the conditional particle-physics interpretation.

## Current status

| Result | Status | Evidence |
|---|---|---|
| Yamamoto Figure 7 extraction | complete | `Yamamoto2020_Fig7.ipynb` and plot in the Python repository |
| Suzaku state and field-integral kernel | complete at the geometry gate | 23-observation cohort and provenance-bearing outputs |
| Source and detection derivation | next | [[next-step]] and the derivation contract |
| Allowed-source viability screen | next | current coupling and invisible-decay constraints |
| Yamamoto spectral and likelihood normalization | open | follows the reviewed derivation |
| DarkNESS reference state table | queued | [[mission-identifiability-work-package]] |
| Field-of-view average | open | follows the accepted on-axis state-table slice |
| Background identifiability | open | uses the nominal and comparison schedules |
| Joint Milky Way and extragalactic calculation | open | source derivation precedes mission analysis |
| Sensitivity envelope | open | follows detector-response and injection gates |

## Gate 1: science definition

The complete source-to-count derivation must reproduce one published
benchmark without a fitted normalization. Current constraints must be applied
to the same combined parameter used in the forecast. The gate records a
continue, revise, or redirect disposition.

## Gate 2: mission state

The reference run must reproduce the commanded boresight, constraint flags,
and conversion kernel for 1,440 ordered samples. The field-of-view calculation
must converge to 1 percent on a declared geometry set. Failure returns the work
to the frame, attitude, or integration model.

## Gate 3: identifiability

The nominal and comparison schedules use the same nuisance hierarchy. The
analysis reports the conversion information before and after nuisance
projection, the lost exposure and slew cost, and the sensitivity to proxy
quality. Failure redirects the paper toward a quantitative requirement for a
particle monitor, control exposure, attitude access, or orbit.

## Gate 4: source components

The Milky Way feature and extragalactic continuum use one parent-decay
normalization and the same response, background cases, and schedule
constraints. The analysis may identify which component contributes more
information, but the physical source model remains joint.

## Gate 5: sensitivity

The sensitivity calculation reports three cases: statistical, reference, and
conservative. Each case includes the parent-decay normalization that permits a
conditional coupling translation. Signal injection must recover the declared
amplitude with acceptable bias and coverage.

## Publication products

The SmallSat package contains the validated kernel, opportunity map, nominal
and comparison timelines, identifiability result, and a sensitivity or
background-requirement surface. The journal package adds the joint-source
calculation, mass dependence, detector response, complete nuisance treatment,
and conditional particle-physics interpretation.

## Links

- charter: [[project-charter]]
- current work: [[next-step]]
- publication scope: [[journal-contribution-scope]]
- literature: [[literature-review]]
- decisions: [[../decisions]]
- open questions: [[../open-questions]]
