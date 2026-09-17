---
type: charter
tags: [darkness, alp, smallsat, project-frame]
created: 2026-09-08
updated: 2026-09-17
status: active
---

# DarkNESS geomagnetic ALP project charter

This note is the canonical project frame. The Python repository contains the
implementation, generated evidence, validation records, and manuscript.

## Research question

Using the DarkNESS platform, what observing ConOps maximises the identifiable
geomagnetic ALP–photon conversion signal against particle and diffuse X-ray
backgrounds, and what does that ConOps require of the mission?

Sub-questions:

1. Which pointing law maximises residual conversion information after
   background regression, under the radiator, limb, slew, and telemetry
   constraints?
2. How much is gained over the nominal sterile-neutrino pointing?
3. What is the cost of umbra-only versus sunlit imaging, and what thermal
   and background evidence would justify sunlit operation?
4. What background monitoring (proxies, control exposures, particle
   monitor) is needed for the signal to remain identifiable?

The ALP ConOps uses DarkNESS as the platform and is not bound to the
sterile-neutrino pointing. Platform constraints still apply. The deliverable
is a ConOps, its gain over nominal pointing, and the mission requirements
that follow. It is not a coupling limit: the provisional reach sits inside
stellar and helioscope bounds, so the coupling question is a conditional
follow-on (see [[research-plan]] result 6).

Superseded question (2026-09-08): whether a DarkNESS-class observation can
place a scientifically new constraint on the combined
decay-and-conversion amplitude for $\chi\rightarrow aa$. Retained as the
journal-extension question.

## Geometry the analysis must own

The signal is set by the line of sight through the magnetosphere, not by a
sky target. $\mathbf B_\perp$ is the field component perpendicular to the line
of sight; the body frame enters only through which directions the aperture
may point. The control variables are orbit position and pointing direction,
both varying each minute. The cosmological ALP flux is isotropic; the Galactic
component scales with dark-matter column density.

The background is not constant. Particle background tracks geomagnetic
position exactly as $B$ does (the central confound, Q7), and diffuse X-ray,
limb, and Sun terms are direction- and time-dependent. The first analysis
product is therefore a per-orbit-sample map of $K(\hat n)$ over the allowed
pointing set with geomagnetic coordinates, limb angle, Sun angle, and eclipse
flag, used to find pointings where $K$ varies while background proxies stay
flat.

## Physical channel

A long-lived, non-relativistic dark-matter parent decays into relativistic
ALPs with keV energies. The ALPs propagate into the magnetosphere and convert
to X-ray photons through the inverse Primakoff effect. The skipper-CCDs measure
the converted photons through their energy deposition in silicon.

The incident ALPs are relativistic daughters of dark-matter decay. They are
not the local cold ALP dark-matter population.

For incident intensity $I_a(E,\hat n)$, the converted brightness is

$$
I_\gamma(E,t,\hat n)=\frac{g_{a\gamma\gamma}^2}{4}
I_a(E,\hat n)K(E,m_a,t,\hat n),
$$

where

$$
K=\left|\int \mathbf B_\perp(\ell,t,\hat n)
\exp\!\left[i\int_0^\ell q(\ell')d\ell'\right]d\ell\right|^2,
\qquad
q=\frac{m_a^2-\omega_{\rm pl}^2}{2E}.
$$

The data directly constrain the incident ALP intensity multiplied by
$g_{a\gamma\gamma}^2$. A coupling-only result requires a declared parent
abundance, lifetime, branching fraction, spectrum, halo model, and cosmology.

## Measurement

For time bin $i$ and reconstructed energy bin $j$, the expected counts are

$$
\mu_{ij}=\theta k_{ij}+\sum_p Z_{ijp}\beta_p,
$$

where $k$ is the response-folded and field-of-view-averaged conversion
template. The matrix $Z$ contains celestial, particle, limb, environment, and
detector-state templates. The coefficient $\theta$ represents the ALP source
normalization multiplied by the coupling dependence.

The useful schedule metric is the information in $k$ after the nuisance
templates have been fitted. In a Gaussian approximation, that information is
proportional to

$$
k^T W^{1/2}(I-P_Z)W^{1/2}k.
$$

The mean or maximum value of $(B_\perp L)^2$ does not determine sensitivity.
A pointing rule has value when it increases the residual conversion
information after lost exposure, slew time, and background covariance are
included.

## DarkNESS reference case

DarkNESS provides four direct-view, fully depleted skipper-CCDs, approximately
12 cm$^2$ of geometric silicon area, a published 20 degree field of view, and
a nominal 1 to 10 keV band. The published mission design also provides the
reference attitude modes, eclipse operations, radiator constraints, orbit
families, data system, and nominal Galactic Centre and Cygnus observations.

The case study uses the current DarkNESS flight design as evidence for a
buildable observatory. An alternative schedule remains a mission-analysis
trade unless the DarkNESS team commits the required observing allocation and
supplies configuration-controlled constraints.

## Source-model gate

The reference two-body decay produces two linked source components.

| Component | Measurement advantage | Measurement cost |
|---|---|---|
| Galactic narrow feature | spectral discrimination and overlap with the nominal Galactic Centre program | dark-matter column density constrains the useful sky directions |
| Cosmological continuum | nearly isotropic incident flux and broad pointing freedom | strong degeneracy with diffuse X-ray backgrounds |

The two components share $f_\chi$, $\tau_\chi$, $\mathcal B_{aa}$, and
daughter multiplicity. The source derivation and reference likelihood include
both. Component-specific mission trades may follow after their separate and
joint information contributions are calculated.

The first gate also asks whether current constraints on invisible dark matter
decay and on $g_{a\gamma\gamma}$ leave any benchmark within DarkNESS reach.
This comparison precedes mission optimization.

## Publication unit

The first publication is a SmallSat 2027 mission-analysis case study.

Provisional title:

> Designing an identifiable geomagnetic ALP search with a skipper-CCD NanoSat:
> DarkNESS as a case study

The paper supports four bounded claims.

1. The field-integral implementation reproduces the Suzaku and Yamamoto
   geometry benchmark.
2. A time-indexed opportunity set represents the published DarkNESS-class
   orbit, attitude, thermal, limb, eclipse, and detector constraints.
3. The residual conversion information provides a common comparison between
   the nominal schedule and one constrained alternative schedule.
4. The result defines a conditional sensitivity or a quantitative requirement
   on background monitoring and control.

The paper does not assert that the current DarkNESS flight mission will
execute the alternative schedule. The paper does not report an
assumption-independent ALP-photon coupling limit. A full spacecraft Geant4
model is outside the minimum publication unit. The analysis instead reports
sensitivity as a function of background reproducibility and proxy quality.

The journal extension adds the phase and plasma mass sweep, full detector
response, tiered background model, injection and coverage tests, multiple
orbit and schedule families, and the conditional particle-physics
interpretation.

## Work breakdown

| Work package | Question | Output | Gate |
|---|---|---|---|
| 0. Canon and inputs | Which quantities are measured, published, adopted, or unresolved? | versioned parameter register | each input has provenance and uncertainty |
| 1. Science definition | Is the source viable and is the full channel normalized correctly? | source card, reviewed derivation, allowed benchmarks, and count screen | one published benchmark is reproduced and a disposition is recorded |
| 2. Suzaku benchmark | Does the conversion kernel reproduce the reference geometry and normalization? | cohort, spectral check, and validation figure | geometry and count normalization pass |
| 3. DarkNESS state table | Which geometries remain accessible under the adopted constraints? | mission state table with nominal pointing and flags | deterministic frame, field, and constraint checks pass |
| 4. Identifiability | Does conversion variation survive the background regression? | nominal and paired-schedule residual information | information remains nonzero under the declared nuisance hierarchy |
| 5. Sensitivity envelope | What combined amplitude can the platform constrain? | ideal, reference, and conservative reach surfaces | injection and coverage tests pass with visible assumptions |
| 6. SmallSat paper | Which mission requirement follows from the result? | paper, figure package, archive, and operations requirements | each claim traces to a versioned output |

## Figure package

1. Measurement concept from parent decay through skipper-CCD response.
2. Suzaku field-integral validation against the Yamamoto benchmark.
3. DarkNESS conversion opportunity map with constraint flags.
4. Nominal and alternative ConOps timelines.
5. Raw and residualized conversion information with background correlations.
6. Sensitivity or required background reproducibility versus observing
   strategy.

## Preliminary scale

For a diffuse background-dominated measurement, the coupling reach scales as

$$
g_{\min}\propto (A\Omega t)^{-1/4}/F_{\rm geom},
$$

where $F_{\rm geom}$ denotes the usable conversion information expressed as an
effective field factor. The current working grasp and exposure values give an
estimated 1.9 to 2.2 improvement in coupling before pointing and systematic
effects. An executable schedule may supply an additional factor of 1.5 to 2
if the selected conversion template remains independent of the background
templates. The resulting 2.8 to 4.4 planning bracket is not a projected limit.

Conditional scaling of the Yamamoto examples gives approximately
$0.75$ to $1.2\times10^{-7}$ GeV$^{-1}$ for the cosmological continuum and
$1.9$ to $3.0\times10^{-8}$ GeV$^{-1}$ for the Galactic feature. These values
inherit Yamamoto's source assumptions and do not extend the coherence mass
range.

These provisional values are substantially weaker than standard stellar and
helioscope bounds on the same photon coupling. They do not establish new
particle parameter space. The science-definition gate must compare the
combined source normalization with current constraints before the project can
claim a worthwhile sensitivity target.

## Schedule

The official SmallSat 2027 dates were not available on 2026-09-08. The 2026
conference used an early-February abstract deadline and a mid-June paper
deadline. Those dates define planning markers until the 2027 call is issued.

| Internal target | Deliverable |
|---|---|
| September 2026 | source-model register, derivation contract, allowed benchmarks, and viability screen |
| October 2026 | independent derivation review and Suzaku count-normalization check |
| November 2026 | 24-hour and representative-duration DarkNESS state-table cases |
| December 2026 | field-of-view average, paired schedule, and identifiability comparison |
| January 2027 | joint-source sensitivity or quantified no-reach result and abstract draft |
| February to May 2027 | robustness tests, injection tests, figures, and manuscript |
| June 2027 planning marker | archived analysis package and final paper |

## Mission-team evidence

The following questions require configuration-controlled information.

1. Does the 20 degree field of view denote the full opening angle?
2. Which body axis defines the aperture, and which roll angles satisfy the
   radiator, Earth, and Sun constraints?
3. May the case study evaluate a bounded dedicated pointing allocation?
4. How do geometric area, active area, masking, and the legacy 8 cm$^2$ and
   20 percent settings map to the flight analysis?
5. Which image and housekeeping quantities can constrain the particle
   background?
6. Does the current Galactic Centre exposure baseline use 0.5 Ms or 1 Ms?

Unknown values remain named analysis cases until an authoritative answer is
available. They do not block the state-table implementation.

## Knowledge boundary

This Notebook tree is authoritative for:

- project framing and publication scope
- physical interpretation and source models
- mission and detector parameter registers
- assumptions, decisions, open questions, and literature synthesis
- work packages and current status.

`Python/darkmatter/ALP` is authoritative for:

- executable analysis code and tests
- input manifests and machine-readable configuration
- generated state tables, plots, summaries, and provenance
- validation records tied to generated outputs
- the manuscript, bibliography, and build products.

A result enters the Notebook after a code output and its provenance have been
reviewed. The Notebook records the interpretation and resulting decision. It
does not duplicate large generated tables or implementation details.

## Sources

- Alpine et al. 2025, *DarkNESS: A skipper-CCD NanoSatellite for Dark Matter
  Searches*: https://arxiv.org/abs/2505.16981
- Alpine et al. 2026, *X-ray characterization of fully-depleted p-channel
  Skipper-CCDs for the DarkNESS mission*:
  https://arxiv.org/abs/2602.02461
- Yamamoto et al. 2020, *A Search for a Contribution from Axion-Like Particles
  to the X-Ray Diffuse Background Utilizing the Earth's Magnetic Field*:
  https://arxiv.org/abs/1906.04429
- IAGA IGRF-14: https://www.iaga-aiga.org/igrf/
- Small Satellite Conference dates:
  https://smallsat.org/conference/dates-and-deadlines/

## Links

- home: [[../ALP]]
- current work: [[next-step]]
- detailed research plan: [[research-plan]]
- decisions: [[../decisions]]
- open questions: [[../open-questions]]
- parameters: [[../00-baseline/darkness-parameters]]
- signal chain: [[../01-physics/alp-signal-chain]]
- derivation contract: [[../01-physics/detection-channel-derivation-contract]]
- sensitivity method: [[../03-sensitivity/method]]
