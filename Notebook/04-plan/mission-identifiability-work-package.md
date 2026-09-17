---
type: work-package
tags: [darkness, alp, mission-analysis, identifiability]
created: 2026-09-08
updated: 2026-09-08
status: queued
---

# Mission identifiability vertical slice

This work package follows the science-definition and derivation gate in
[[next-step]]. It determines whether a DarkNESS-class schedule can create
geomagnetic conversion contrast that remains distinguishable from orbital
background drivers.

## Reference case

| Quantity | Adopted value |
|---|---:|
| Orbit | circular ISS-like LEO |
| Altitude | 420 km |
| Inclination | 51.6 degrees |
| Epoch | 2027-01-01 00:00:00 UTC |
| Initial duration | 24 hours |
| Extended duration | 30 days after acceptance |
| Cadence | 60 s |
| Nominal pointing | Galactic Centre when accessible |
| Comparison pointing | one constrained high and low conversion rule |
| Initial conversion | coherent, on-axis |
| Field of view | published 20 degree value carried as metadata, followed by a converged average |

The initial orbital phase and RAAN are simulation seeds. The extended run must
sample or marginalize them before a mission conclusion is reported.

## Required state

Each sample records epoch, inertial and Earth-fixed spacecraft state,
geodetic coordinates, boresight, roll, target access, Earth intersection,
limb angle, eclipse state, Sun angle, environment flags, background proxies,
slew state, science live state, conversion kernel, and model provenance.

## Analyses

1. Verify frames, pointing, Earth intersection, and constraint flags.
2. Calculate the on-axis conversion-kernel distribution during usable
   exposure.
3. Establish field-of-view quadrature that converges to 1 percent.
4. Construct a hierarchy of background design matrices.
5. Calculate correlation, variance inflation, and residual conversion
   information for the nominal schedule.
6. Generate one feasible high and low conversion schedule.
7. Compare information gain after exposure and slew losses.
8. Repeat the calculation with the accepted joint source template from the
   derivation gate.

## Acceptance

- The 24-hour run contains 1,440 ordered samples with explicit units.
- Repeated runs produce identical state and kernel values.
- Boresight and Earth-intersection tests pass known cases.
- At least 99 percent of valid rays meet numerical convergence.
- The field-of-view average meets the 1 percent convergence criterion.
- Results include a declared nuisance hierarchy.
- Each mission constraint is labeled published, adopted, or unresolved.

## Disposition

**Continue:** residual conversion information survives plausible nuisance
models. Proceed to a representative-duration sensitivity envelope.

**Revise:** information survives only with stronger proxy, calibration, or
control-exposure performance. Convert the result into a mission requirement.

**Redirect:** each feasible schedule leaves the signal template collinear
with plausible background drivers. Stop the coupling projection and state the
required platform change.

## Links

- prerequisite: [[next-step]]
- charter: [[project-charter]]
- pointing: [[../02-mission-analysis/pointing-optimization]]
- sensitivity: [[../03-sensitivity/method]]
