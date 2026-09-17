---
type: work-package
tags: [darkness, alp, science-definition, derivation, viability]
created: 2026-07-31
updated: 2026-09-08
status: ready
---

# Science-definition and detection-channel gate

## Decision

Pause additional mission optimization until the physical source, conversion,
detector, and inference chain has one reviewed normalization and at least one
scientifically allowed benchmark has been compared with DarkNESS reach.

The geomagnetic geometry kernel is validated at the Suzaku cohort level. The
highest-leverage unresolved issue is now whether the complete channel defines
an observable and worthwhile measurement.

## Research question to resolve

Can a DarkNESS-class observation place an identifiable and scientifically new
constraint on the combined amplitude

$$
\Theta=g_{a\gamma\gamma}^{2}
\frac{f_\chi\mathcal B_{aa}}{\tau_\chi}
$$

for relativistic ALPs from $\chi\rightarrow aa$, after both linked source
components, geomagnetic conversion, detector response, and orbital-background
covariance are included?

When $\tau_\chi$ is not much longer than the age of the universe, it also
changes the extragalactic template. The forecast must then retain lifetime as
a shape parameter in addition to the displayed normalization.

If current constraints place every allowed benchmark below the reachable
count rate, the work package must quantify the gap and identify the platform
or measurement change needed to close it.

## Questions that must be answered

1. What parent-decay parameter space is currently allowed by cosmology,
   structure growth, and direct or indirect searches?
2. What current limits apply to $g_{a\gamma\gamma}$ in the ALP mass range that
   remains coherent in the geomagnetic field?
3. What are the correctly normalized Milky Way and extragalactic ALP
   intensities from the same two-body decay model?
4. What relative count contribution does each linked component make after
   the DarkNESS response and observing geometry?
5. Which geomagnetic, external-magnetosphere, plasma, and absorption models
   are required at the accuracy of the projected result?
6. What count-level parameter combination is identifiable without fixing the
   parent abundance, lifetime, and branching fraction?
7. Does an allowed benchmark produce enough counts to justify mission
   optimization?
8. Which mission variables materially change the answer?

## Tasks and outputs

### Task 1: source-model and constraint card

Define $m_\chi$, $m_a$, $f_\chi$, $\tau_\chi$, $\mathcal B_{aa}$,
$g_{a\gamma\gamma}$, the halo profile, and cosmology. Record current
constraints and select an optimistic allowed, reference allowed, and
conservative benchmark.

Output: a provenance-bearing source-model table with no hidden unit or density
conventions.

### Task 2: source derivation

Derive the Milky Way feature and extragalactic continuum from
$\chi\rightarrow aa$. Track daughter multiplicity, solid-angle factors,
redshift Jacobians, decay history, halo velocity broadening, and the shared
normalization.

Output: a symbolic derivation and benchmark spectra that reproduce a primary
source without a fitted scale.

### Task 3: conversion derivation

Derive weak ALP-photon mixing in a spatially varying magnetic field and
plasma. Establish the two-polarization vector amplitude, phase convention,
path direction, boundaries, and unit conversion.

Output: analytic limiting cases and tests specified in
[[../01-physics/detection-channel-derivation-contract]].

### Task 4: detector forward model

Carry both source components through projected area, aperture acceptance,
field-of-view integration, quantum efficiency, live and masked fractions,
energy redistribution, event selection, and radiation-age response.

Output: counts per time and energy bin for the three source benchmarks and
one transparent toy background.

### Task 5: scientific viability screen

Compare the expected count amplitude for allowed benchmarks with statistical
and background-reproducibility floors. Express the result first in $\Theta$,
then as a conditional coupling curve.

Output: one plot showing allowed source benchmarks, DarkNESS reach, existing
constraints in the same parameterization, and the factor separating them.

### Task 6: inference and mission traceability

Define the likelihood, nuisance hierarchy, confidence construction, and
residualized information metric. Map each sensitivity driver to a measurable
mission requirement.

Output: the first science-to-measurement-to-requirement traceability table.

### Task 7: independent derivation review

Prepare the bounded review packet described in the derivation contract. Ask
Astra to identify the first invalid step, missing factor, inconsistent unit,
or unsupported approximation. Resolve findings before the mission-state work
package begins.

Output: review disposition and corrected derivation version.

## Acceptance

- Source spectra recover one published benchmark without arbitrary rescaling.
- Conversion code passes constant-field, coherent, sign-changing-field, basis,
  and convergence tests.
- Detector count units reduce to counts per bin.
- The leading signal normalization is $g_{a\gamma\gamma}^{2}$, not
  $g_{a\gamma\gamma}^{4}$, when the parent decay rate is an independent input.
- All existing-constraint comparisons use the same source assumptions and
  parameter combination.
- At least one allowed benchmark and its expected DarkNESS counts are shown.
- A continue, revise, or redirect disposition is recorded.

## Mission-intent outputs

The gate must set, bound, or explicitly defer:

- energy band and energy-resolution requirement
- grasp and effective-area requirement
- useful live exposure and cadence
- boresight, roll, sky-access, slew, and settle requirements
- limb, Sun, eclipse, and occultation constraints
- attitude, orbit, and time-knowledge accuracy
- background reproducibility
- particle and environment proxy accuracy
- required calibration and control observations
- detector-state and housekeeping telemetry.

## Disposition

**Continue:** an allowed benchmark is reachable or the mission improves a
constraint on $\Theta$. Begin [[mission-identifiability-work-package]].

**Revise:** no new particle parameter space is reached, but the analysis can
produce a quantitative no-reach result, method validation, or future-platform
requirement suitable for a SmallSat mission-analysis paper.

**Redirect:** the source is unobservable by a wide-field LEO X-ray detector
under all credible cases and no distinctive mission-analysis question remains.

## Links

- derivation contract: [[../01-physics/detection-channel-derivation-contract]]
- queued mission analysis: [[mission-identifiability-work-package]]
- charter: [[project-charter]]
- research plan: [[research-plan]]
- open questions: [[../open-questions]]
