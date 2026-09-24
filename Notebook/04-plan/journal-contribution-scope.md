---
type: plan
tags: [darkness, alp, journal, scope, mission-analysis]
created: 2026-07-30
updated: 2026-09-08
status: active
---

# Publication scope

The governing project frame is [[project-charter]].

## SmallSat 2027

The first publication evaluates whether a DarkNESS-class skipper-CCD NanoSat
can create an identifiable geomagnetic ALP measurement under executable
operations constraints. The analysis compares the nominal observing program
with one constrained high and low conversion schedule. It reports the
conversion information that remains after orbit and background covariates are
fitted.

The SmallSat result is useful under either disposition. A positive feasibility
result defines the sensitivity and observing requirements. A negative result
defines the background monitoring, control mode, attitude access, or orbit
change required by a future mission.

The current flight mission provides the reference platform and nominal ConOps.
An alternative schedule remains a case-study trade until the DarkNESS team
commits observing time and supplies configuration-controlled constraints.

## Journal extension

The journal paper adds the source-normalized particle-physics interpretation
after the mission-analysis result is stable. It includes the phase-aware mass
sweep, plasma and field-model cases, full energy-dependent detector response,
tiered background model, multiple orbit and schedule cases, and signal
injection with coverage tests.

The Milky Way feature and extragalactic continuum are linked components of
the same two-body decay source. The reference likelihood includes both with a
shared decay normalization. Their separate information contributions may be
reported to explain the mission design.

## Claim boundary

The measurement directly constrains the incident ALP intensity multiplied by
$g_{a\gamma\gamma}^2$. A coupling-only curve is conditional on the parent
dark-matter abundance, lifetime, branching fraction, halo model, and
cosmology.

The publication does not claim sensitivity to cold ALP dark matter. It does
not treat an absolute diffuse X-ray excess as evidence for conversion. A
candidate signal must reproduce the adopted spectral template and the
calculated geomagnetic time dependence.

## Publication gates

Status 2026-09-24: gate 1 met by [[../03-sensitivity/result]]; the viability screen returned Revise (D31).

1. The source-to-count derivation reproduces a published benchmark and the
   viability screen includes current constraints.
2. The Suzaku geometry and spectral normalization reproduce the declared
   Yamamoto benchmarks.
3. The DarkNESS field of view, effective area, live fraction, and current
   exposure case have controlled provenance.
4. The mission-state calculation produces a constrained nominal schedule and
   one comparison schedule.
5. The conversion template remains identifiable under a declared hierarchy of
   particle and celestial background models.
6. The linked source components use a common count model and shared
   normalization.
7. Signal injection and coverage tests pass before the sensitivity curve is
   reported.

## Paper assets

The manuscript, bibliography, build script, and rendered paper belong in
`Python/darkmatter/ALP/paper`. This note owns the publication claim and scope.

## Links

- charter: [[project-charter]]
- current work: [[next-step]]
- research plan: [[research-plan]]
- pointing: [[../02-mission-analysis/pointing-optimization]]
- sensitivity: [[../03-sensitivity/method]]
- open questions: [[../open-questions]]
