---
title: Literature Review - DarkNESS LEO Diffuse X-ray Mission Design for Geomagnetic ALP Conversion
status: working review v0.1
updated: 2026-09-08
---

# Literature Review

This note is the canonical literature synthesis. [[project-charter]] controls
the current claim boundary and [[next-step]] controls the active work. Earlier
recommendations below remain evidence history when they differ from those two
notes.

## Review purpose

This is a scoped, claim-driven review for a journal contribution at the intersection of space systems engineering, diffuse X-ray measurement, and axion-like particle (ALP) physics. It asks whether the DarkNESS 6U skipper-CCD observatory can support a defensible search for X-rays produced by ALP conversion in the Earth's magnetic field, and what new mission-analysis method is required to make that search credible.

The review is intentionally narrower than a general review of axions, dark matter, CubeSats, or X-ray astronomy. A source is included when it supports at least one of four analysis needs:

1. the ALP source and conversion model;
2. the DarkNESS detector and operational boundary;
3. a usable celestial or non-X-ray background model; or
4. a precedent for converting orbit, attitude, and detector-state variables into a controlled measurement.

## Provisional research framing

The paper should be framed as a space-systems and measurement-design study with an ALP demonstration case:

> How can a wide-field, non-imaging skipper-CCD nanosatellite use orbit and pointing as experimental controls for a weak diffuse X-ray signal when the instrumental background is itself orbit dependent?

The ALP case is especially valuable because its predicted amplitude varies with a calculable line-of-sight geomagnetic regressor, approximately $(B_\perp L)^2$ in the coherent regime. This turns the observing schedule into part of the experiment. The research contribution is not merely a new sensitivity curve; it is a traceable chain from orbit and attitude constraints to signal leverage, background covariance, and a projected limit.

## Review questions

- RQ1: What ALP flux and conversion assumptions are required to reproduce the Yamamoto et al. benchmark?
- RQ2: Which DarkNESS response parameters are measured, published, assumed, or still unresolved?
- RQ3: Which background components matter in the 2-6 keV validation band and the broader 1-10 keV DarkNESS band?
- RQ4: Which accessible models or archives can initialize those background components before DarkNESS flight data exist?
- RQ5: Which orbit- and attitude-dependent variables must be carried into the likelihood and the scheduling objective?
- RQ6: What result would constitute a generalizable space-systems contribution rather than a dark matter-only forecast?

## Synthesis

### 1. The physics benchmark is established, but the observing geometry was not designed for it

Yamamoto et al. searched Suzaku blank-sky spectra for an X-ray component proportional to the line-of-sight geomagnetic conversion strength. They found no evidence and reported a 99% confidence upper limit on the residual 2-6 keV surface brightness, normalized at $10^4$ T2 m2. Their analysis is the correct benchmark because it combines the same Earth-field conversion mechanism, a LEO X-ray CCD, time-resolved orbit data, and an explicit non-X-ray-background treatment.

The paper also exposes the central systems opportunity. Suzaku observations were selected from an archive; their pointing and orbital sampling were not chosen to maximize ALP information. DarkNESS can potentially choose or prioritize observations. The relevant design variable is not simply the maximum value of $(B_\perp L)^2$, but the weighted spread of that value across observations after accounting for nuisance variables.

Marsh et al. provide a more general phase-aware treatment of photon-ALP conversion in arbitrary magnetic fields and an efficient Fourier interpretation. That work supports retaining the full complex line integral for the final mass-dependent calculation while using the coherent approximation for initial mission-design sweeps.

### 2. DarkNESS supplies a credible detector platform, but not yet a complete LEO background spectrum

The published DarkNESS design establishes the 6U platform, four skipper-CCDs, wide field of view, 1-10 keV science band, LEO orbit families, and eclipse-centered operations. The lack of focusing optics gives low source-imaging capability but substantial grasp for diffuse emission. The same paper makes clear that LEO radiation and particle-induced low-energy events are major challenges.

Two newer DarkNESS-adjacent results materially improve the starting point. Gaido et al. provide a laboratory-calibrated model of cosmic-ray-induced Cherenkov photons in low-noise silicon detectors and show dependencies on silicon thickness, solar activity, particle species, and track masking. Alpine et al. quantify X-ray response degradation after proton irradiation for fully depleted p-channel skipper-CCDs. These results mean the detector portion of the background and response model should not be represented by a single generic efficiency. It should carry energy response, masking/live fraction, radiation age, and particle-track observables separately.

Neither paper supplies a complete DarkNESS LEO count spectrum. That is not a fatal gap for a feasibility study. It means the projection must distinguish between environment specification, detector transport, empirical calibration, and nuisance uncertainty instead of treating one inherited spectrum as truth.

### 3. LEO X-ray missions support a covariate-based background strategy

Suzaku provides the closest direct precedent. Tawa et al. constructed non-X-ray-background spectra from night-Earth data and sorted them by cutoff rigidity or an onboard particle-monitor proxy. Their results show both the value and limitation of a single geomagnetic predictor: background reproducibility improved substantially, but geographic and long-term residual structure remained. Yamamoto then identified the precise confounding problem relevant here: $(B_\perp L)^2$ and particle background can both depend on orbital position.

NICER provides a modern non-imaging precedent. Its 3C50 model uses empirical library spectra indexed by measurements not contaminated by the science target. The current NICER toolchain also offers parameterized SCORPEON and a Space Weather model. The important lesson is architectural: faint-source background is represented by components or empirical states linked to housekeeping and environmental predictors, with explicit filtering when the predictors do not support a reliable estimate. NICER spectra are not directly transferable to a skipper-CCD, but the modeling pattern is.

HaloSat is the strongest small-satellite analogue. It used a wide field of view to measure diffuse soft X-rays from a 6U platform and fitted separate astrophysical, CXB, local-hot-bubble, and particle-induced detector components. Its background documentation records that the original particle-background model was incomplete and was revised to include a second low-energy power law. This is a useful warning against assuming that one smooth instrumental continuum will remain adequate at DarkNESS energies.

Together, these missions support a hybrid DarkNESS strategy: physics-informed component shapes before flight, broad nuisance parameters in the projection, operational filtering based on orbit and detector proxies, and an empirical background library built from commissioning and control observations after launch.

### 4. Accessible models exist, but they answer different questions

The available resources should not be collapsed into one "background model":

- Celestial sky: the existing Micro-X GC/off-plane templates can initialize spectral studies. Public ROSAT/Wisconsin diffuse-background maps can supply direction-dependent sky priors, including a historical 1.8-6.3 keV all-sky band, although their angular and spectral resolution are coarse and their instrument response differs from DarkNESS.
- Trapped particles: AE9/AP9/SPM or SPENVIS can specify proton/electron flux distributions along candidate orbits. These are environment models, not detector count spectra.
- Detector transport: Geant4 is the appropriate bridge from incident particle fields and spacecraft geometry to energy deposits, fluorescence, secondary particles, tracks, and masks. It requires a credible spacecraft/payload mass model.
- Solar-wind foregrounds: solar wind charge exchange is temporally variable and difficult to predict precisely. It should enter through spectral nuisance components, observing constraints, and solar-wind proxies rather than a single deterministic subtraction.
- Empirical calibration: night-Earth, Earth-blocked, blank-sky, high-energy-track, overscan, masking-fraction, and detector-state data can constrain the preceding components once flight data exist.

The literature therefore supports a staged model. A preflight mission projection can use accessible sky maps, environment fluxes, detector-response measurements, and conservative uncertainty envelopes. A final flight analysis would replace or constrain these components with DarkNESS-specific empirical states.

### 5. The literature gap is a mission-design and identifiability problem

No reviewed source closes the full loop for DarkNESS:

`orbit and attitude -> geomagnetic ALP regressor -> background covariates -> constrained schedule -> profile likelihood -> projected limit`.

That loop is the candidate journal contribution. Its novelty rests on three requirements:

1. treat the schedule as an experimental design rather than an exposure accumulator;
2. optimize information after profiling nuisance components, not maximum field strength; and
3. quantify whether the ALP regressor is identifiable from cutoff rigidity, geographic position, limb angle, eclipse state, solar conditions, and detector state.

If the signal regressor cannot be decorrelated from the background predictors, that negative feasibility result is itself meaningful. It defines a systems requirement for a future mission, such as an onboard particle monitor, a shutter/control mode, different orbit selection, or paired attitude states.

## Proposed objectives

### Objective 1 - Establish the validated physics and response baseline

Reproduce Yamamoto's field-integral scale and Figure 7 limit using the published Suzaku configuration. Reconcile the DarkNESS geometric area, silicon thickness, quantum efficiency, energy resolution, FOV convention, masking, and exposure assumptions with the existing `LimitCalculation` implementation.

### Objective 2 - Build the mission-analysis state table

For representative ISS-like and SSO cases, generate frame-level orbit, eclipse, occultation, limb, attitude, geomagnetic, space-weather, detector-state, and $(B_\perp L)^2$ variables. The state table is the common interface between mission simulation, background estimation, scheduling, and inference.

### Objective 3 - Construct a tiered background model

Implement separate celestial, particle-induced, limb/albedo, SWCX, and detector-state components. Carry three evidence levels: a statistical lower bound, a physics/heritage-informed operational model, and a conservative systematic floor. Do not transfer NICER, HaloSat, or Micro-X count spectra as if they were DarkNESS calibration data.

### Objective 4 - Design and compare executable observing strategies

Compare the opportunistic baseline, fixed inertial pointing, maximum-field tracking, stepped scanning, and matched high/low conversion pairs. Include slew/settle, eclipse, thermal, power, radiator, limb, SAA, data-volume, and detector-live-time constraints.

### Objective 5 - Produce a systematics-aware sensitivity projection

Fit the time-energy correlation model, profile the background components, perform injection/recovery tests, and place projected DarkNESS lines on the Yamamoto Figure 7 axes. Report how sensitivity changes with background knowledge and observing strategy, not only one headline curve.

## Claim-evidence matrix

| ID | Source | Evidence contributed | Limitation / caution | Use in this work |
|---|---|---|---|---|
| M1 | Alpine et al. 2025, DarkNESS mission | Published instrument, platform, response goals, orbit domains, ConOps, and sensitivity assumptions | Several values remain design-dependent; LEO particle model was ongoing | Canonical DarkNESS baseline |
| M2 | Alpine et al. 2026, irradiated skipper-CCD X-ray response | Proton-damage test and end-of-life resolution basis for representative LEO cases | Preprint and accelerated test; not a full on-orbit background measurement | Time-dependent response and uncertainty |
| P1 | Yamamoto et al. 2020 | Earth-field ALP method, Suzaku benchmark, 2-6 keV limit, background-confounding precedent | Archival pointings; analysis tied to Suzaku response and fields | Primary validation target |
| P2 | Marsh et al. 2021 | Full phase-aware conversion in arbitrary fields and Fourier acceleration | General formalism, not Earth-mission-specific | Final conversion kernel and mass reach |
| B1 | Tawa et al. 2008 | Night-Earth NXB database; cutoff-rigidity and particle-monitor predictors; reproducibility tests | Suzaku-specific detector and particle monitor | Background architecture and validation metric |
| B2 | Remillard et al. 2021 | Empirical NICER library model indexed by target-independent detector proxies; GTI quality filtering | NICER detector/background states cannot be copied to DarkNESS | Empirical-library design precedent |
| B3 | HEASARC NICER SCORPEON documentation | Parameterized, library, and space-weather models coexist; fittable component approach | Operational documentation, not independent DarkNESS evidence | Software architecture precedent |
| B4 | HaloSat analysis guide and background memo | Wide-FOV 6U diffuse-X-ray decomposition; particle background required two power laws | 0.4-7 keV SDD response and HaloSat orbit differ | Closest small-satellite measurement analogue |
| B5 | Kuntz 2019 | SWCX is ubiquitous, variable, and difficult to subtract without matched observations | Strongest below the primary 2-6 keV validation band, but still relevant | Foreground nuisance and scheduling |
| B6 | Snowden et al. ROSAT diffuse maps / HEASARC | Public direction-dependent soft-X-ray maps and uncertainties | Coarse spectrum, historical calibration, point-source treatment varies | Initial sky prior and pointing screen |
| E1 | Ginet et al. 2013, AE9/AP9/SPM | Statistical trapped electron/proton/plasma environment specification | Produces environment flux, not DarkNESS CCD events | Orbit-dependent particle input |
| E2 | Agostinelli et al. 2003, Geant4 | General particle transport toolkit used for detector-background simulation | Accuracy depends on geometry, materials, source spectra, and validation | Particle-to-detector transfer model |
| D1 | Gaido et al. 2025 | Laboratory-calibrated cosmic-ray Cherenkov model for low-noise silicon; thickness, solar, species, masking dependencies | Primary application is not DarkNESS LEO X-ray spectroscopy | DarkNESS-specific low-energy background component |
| A1 | Figueroa-Feliciano et al. 2015 | GC diffuse-X-ray model underlying the existing sterile-neutrino calculation | GC-specific and designed for a different detector/measurement | Heritage sky template, not universal background |

## Proposed introduction structure

1. Weak diffuse X-ray measurements are often limited by environment-dependent backgrounds rather than detector read noise alone.
2. Wide-field small satellites such as HaloSat and non-imaging instruments such as NICER demonstrate both the value of high grasp and the need for covariate-based background estimation.
3. DarkNESS extends this design space with skipper-CCDs and a science case in which LEO geometry modulates the expected signal itself.
4. Yamamoto established the geomagnetic ALP method with Suzaku but could not design the observation geometry for that measurement.
5. The unresolved problem is whether a constrained DarkNESS schedule can increase signal leverage without creating degeneracy with geomagnetically driven backgrounds.
6. This work develops, validates, and applies a mission-design framework to answer that question and produce a systematics-aware sensitivity projection.

## Immediate research gaps

1. The 20-degree FOV convention and aperture-body-axis definition remain unresolved.
2. The legacy 8 cm2 / 20% `LimitCalculation` configuration is not reconciled with the published 12 cm2 area, QE, and masking assumptions.
3. No DarkNESS-specific LEO event-spectrum model has been identified. The status and accessibility of the Fermilab Geant4 geometry and Gaido background implementation should be established.
4. The available onboard proxies for particle environment and detector state are not yet defined. An onboard particle monitor may not exist, making track rate, rejected-event rate, or image morphology particularly important.
5. A matched control-observation mode is not yet part of the published ConOps.
6. The covariance between $(B_\perp L)^2$ and cutoff rigidity has not been calculated for any candidate DarkNESS schedule.

## First committed technical work package

The first implementation should be a validation-and-state-table package, not the complete background simulator:

1. reproduce the Yamamoto field integral for one Suzaku observation already present in `data/suzaku`;
2. define a documented frame-state schema containing time, position, attitude, eclipse, limb, cutoff-rigidity proxy, $(B_\perp L)^2$, exposure, and quality flags;
3. generate that table for one representative DarkNESS orbit and a small boresight grid;
4. plot $(B_\perp L)^2$ against cutoff rigidity and orbital position; and
5. determine whether matched high/low conversion observations exist before adding spectral backgrounds.

This package tests the paper's central premise with minimal dependence on uncertain background amplitudes.

## Core sources

- [Alpine et al. 2025, DarkNESS mission](https://doi.org/10.1016/j.asr.2025.07.070)
- [Alpine et al. 2026, skipper-CCD X-ray response after proton irradiation](https://arxiv.org/abs/2602.02461)
- [Yamamoto et al. 2020, geomagnetic ALP conversion with Suzaku](https://doi.org/10.1088/1475-7516/2020/02/011)
- [Marsh et al. 2021, Fourier formalism for photon-ALP conversion](https://arxiv.org/abs/2107.08040)
- [Tawa et al. 2008, Suzaku XIS non-X-ray background](https://arxiv.org/abs/0803.0616)
- [Remillard et al. 2021, NICER empirical background model](https://arxiv.org/abs/2105.09901)
- [HEASARC NICER background-model overview](https://heasarc.gsfc.nasa.gov/docs/nicer/analysis_threads/scorpeon-overview/)
- [HaloSat analysis guide](https://heasarc.gsfc.nasa.gov/docs/halosat/analysis/halosat_analysis_20220214.pdf)
- [HaloSat background analysis memo](https://heasarc.gsfc.nasa.gov/docs/halosat/analysis/back20221130.pdf)
- [Kuntz 2019, solar-wind charge exchange review](https://arxiv.org/abs/1811.06454)
- [HEASARC soft X-ray background data resources](https://heasarc.gsfc.nasa.gov/docs/heasarc/xrayback.html)
- [Ginet et al. 2013, AE9/AP9/SPM environment models](https://doi.org/10.1007/s11214-013-9964-y)
- [Agostinelli et al. 2003, Geant4](https://doi.org/10.1016/S0168-9002(03)01368-8)
- [Gaido et al. 2025, Cherenkov background in low-noise silicon](https://arxiv.org/abs/2507.00226)
- [Figueroa-Feliciano et al. 2015, Micro-X sterile-neutrino search model](https://doi.org/10.1088/0004-637X/814/1/82)



## Notebook links

- project charter: [[project-charter]]
- current work: [[next-step]]
- open questions: [[../open-questions]]
- decisions: [[../decisions]]
