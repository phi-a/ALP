---
type: moc
tags: [moc, darkness, alp]
created: 2026-06-22
updated: 2026-09-17
status: active
---

# ALP

Canonical project charter: [[04-plan/project-charter]].

Literature basis: [[04-plan/literature-review]].

Current work package: [[04-plan/next-step]].

Journal framing: [[04-plan/journal-contribution-scope]].

Requirements: [[04-plan/alp-baseline-requirements]].

> Home note for a DarkNESS case study of geomagnetic conversion of relativistic ALPs produced by
> dark-matter decay, benchmarked against Yamamoto et al. 2020.

## The one-paragraph version

A heavier dark-matter parent may decay to relativistic, keV-energy ALPs. The
same decay produces a Milky Way feature and an extragalactic continuum. The
ALPs can convert to X-ray photons in the Earth's magnetic field. DarkNESS may
test the resulting time-, direction-, and energy-dependent photon template.
The immediate research question is whether the full channel is normalized
correctly and whether any currently allowed source benchmark is reachable.
Mission pointing and identifiability follow that gate. A conditional coupling
curve is a downstream translation.

## Two lines of work

**The DarkNESS-precise line** (`00-` … `04-`) — every parameter traceable to the mission, provenance-tagged.
This is the line that produces a defensible sensitivity projection.

**The general survey** — [[darkness_alp]], the broad LEO-SmallSat ALP mission-class study. Prior art, kept
intact, treats DarkNESS as one option among several. Do not mix its trade-study numbers into the precise
line. See [[decisions]] D1.

## Start here

- [[00-baseline/darkness-parameters|Parameter register]] — **the canonical numbers.** If it is not here, it is not real
- [[04-plan/project-charter|Project charter]] — canonical framing,
  publication split, gates, and schedule
- [[04-plan/next-step|Current work package]] — science definition,
  derivation, and viability gate
- [[04-plan/mission-identifiability-work-package|Queued mission work]] — the
  DarkNESS identifiability vertical slice
- [[04-plan/research-plan|Research plan]] — current result sequence and gates
- [[open-questions|Open questions]] — Q1 and Q2 are answerable today and scale every result

## Baseline

- [[00-baseline/darkness-parameters|Parameters]] — instrument, platform, environment, with provenance tags
- [[00-baseline/skipper-ccd|Skipper-CCD sheet]] — area, FOV, QE, resolution, selection, and where each enters the count model
- [[00-baseline/darkness-conops|ConOps as constraints]] — umbra-only vs sunlit trade, two-axis attitude, the eclipse trade

## Physics

- [[01-physics/alp-signal-chain|Signal chain]] — linked source components, conversion probability, and counts model
- [[01-physics/derivation-sources|Derivation sources]] — origin equations, notation map, DarkNESS inputs and checks per block
- [[01-physics/block-a-conversion|Block A: conversion]] — the amplitude from the mixing equations, validity, ray geometry, units, six checks
- [[references|References]] — the one keyed bibliography
- [[01-physics/detection-channel-derivation-contract|Derivation contract]] — equations, assumptions, tests, and review gate
- [[01-physics/coherence-and-mass-reach|Coherence and mass reach]] — why the mass axis is not a design variable
- [[01-physics/sensitivity-scaling|Sensitivity scaling]] — grasp, exposure, geometry, and covariance

## Mission analysis

- [[02-mission-analysis/conops-physics-map|ConOps ↔ physics map]] — what each ConOps variable touches; pointing tiers by mission cost; occultation as the free "off" state
- [[02-mission-analysis/geomagnetic-integral|Field integral]] — the one new module; definitions and the validation gates, which pass
- [[02-mission-analysis/pointing-optimization|Pointing optimisation]] — **the research element**; where the field actually is, measured
- [[02-mission-analysis/orbit-cases|Orbit cases]] — ISS-like, SSO noon/midnight, SSO dawn/dusk
- [[02-mission-analysis/pointing-system|Pointing system]] — target → mode → schedule → steering → boresight; the ritual every run declares
- [[02-mission-analysis/testing|Testing]] — the five layers, what each catches, and the four bugs they found
- [[02-mission-analysis/api-reference|API reference]] — every public function, generated from the docstrings
- [[02-mission-analysis/tooling|Tooling]] — the numpy/scipy/astropy library by topic, known-answer checks, speed, first run

## Sensitivity

- [[03-sensitivity/method|Method]] — reuse of the `LimitCalculation` chain, and why it must be a correlation measurement

## Student project

- [[05-student/project-pathway|Project pathway]] — seven stages, one figure each, written for the student
- [[05-student/mentor-guide|Mentor guide]] — how to run it, where the difficulty really is, what to hold back

## Process

- [[decisions|Decision log]] — append-only, with reversal conditions
- [[open-questions|Open questions]] — blocking and non-blocking

## External artifacts

- `darkmatter/ALP/Yamamoto2020_Fig7.ipynb` — Figure 7 replication, validated by digitising the published figure
- `darkmatter/LimitCalculation` — sterile-neutrino sensitivity chain to be reused
- [[Designing and Simulating a LEO SmallSat ConOps for Reverse-Primakoff ALP Sensitivity.pdf]] — source PDF for [[darkness_alp]]
- Alpine et al. 2025, *DarkNESS: A skipper-CCD nanosatellite for dark matter searches*, ASR 76, 4793

## Links

- parent: [[../DarkNESS]]
- me: [[Phi]]
