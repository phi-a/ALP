---
type: note
tags: [darkness, alp, mission-analysis, tooling]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# Tooling decision: Python stack, not an astrodynamics platform

**Decision: piece it together in Python.** GMAT, STK, and Orekit solve problems this study does not have,
and do not solve the one problem it does have.

## Why the heavy tools do not fit

**This is a design study, not operations.** We need the *statistical distribution* of accessible
$(B_\perp L)^2$ over a representative year, not the predicted position of a specific spacecraft at a
specific second. A position error of a few km is irrelevant — the geomagnetic field varies over hundreds
of km. The precision those tools exist to provide is precision we would throw away.

**The one hard piece is not in any of them.** The line-of-sight IGRF integral
([[geomagnetic-integral]]) is custom work regardless of platform. GMAT and Orekit do not model the
geomagnetic field for this purpose; STK's magnetic modules are not built for line-of-sight integration
either. We write that module either way.

**We need pointing geometry, not attitude dynamics.** No reaction-wheel simulation, no momentum
management, no control loops. Just a unit vector plus constraint checks (Sun angle, Earth limb, umbra,
radiator direction). This is the point where people reach for STK and should not.

**No maneuvers, no station-keeping, no covariance, no collision avoidance.** Those are the things that
justify a real astrodynamics platform. We have none of them.

## The one place fidelity genuinely matters

**J2 nodal precession, for the sun-synchronous cases.** A sun-synchronous orbit is *defined* by its nodal
regression matching Earth's mean motion about the Sun. Propagate it with plain two-body Keplerian motion
and the orbit plane will not precess, the local time of ascending node will drift away from its design
value over the year, and the eclipse fractions and beta-angle behaviour — which drive the whole umbra
trade in [[orbit-cases]] — will be wrong.

This is free if you use SGP4 (which includes secular J2) or apply the analytic nodal regression directly.
It is a silent, serious error if you hand-roll a circular orbit and forget it. Worth an explicit check:
propagate an SSO for a year and confirm the LTAN holds to within minutes.

## Recommended stack

| Package | Role | Note |
|---|---|---|
| `skyfield` | Time systems, frame transforms, Sun/Earth ephemeris, SGP4 | Beginner-friendly docs, actively maintained. Use it for frames — do not hand-roll |
| `ppigrf` | IGRF-13/14 field model | Pure Python, numpy-vectorised, one function call |
| `numpy`, `scipy`, `matplotlib` | Everything else | Already installed |
| `astropy` | Units, coordinates if wanted | Already installed |

Avoid `poliastro` — development stopped and it forked to `hapsira`; not a good dependency for a student
project. Avoid `orekit` (Java-backed, heavy install, steep curve) unless the project outgrows Python,
which it will not.

## Where the actual risk is

Not propagator accuracy. **Coordinate frames and time systems.** Inertial vs Earth-fixed vs geodetic
lat/lon/alt, and UTC vs UT1 vs TT. This is the dominant bug source in the whole project and it produces
results that look plausible.

Which is the argument *for* using a tested library rather than writing transforms by hand — and for two
cheap validation gates:

1. **IGRF check.** Evaluate the field at a known latitude, longitude, and altitude and compare against
   NOAA's online geomagnetic calculator. Catches nearly every frame error immediately.
2. **Orbit check.** Propagate a real TLE and compare against a second source. GMAT is free and scriptable
   — using it *once* as a cross-check, rather than as the platform, is a reasonable middle path if a
   controlled tool is wanted in the loop for credibility.

The South Atlantic Anomaly appearing in the right place (Stage 2 of [[../05-student/project-pathway]]) is
the same gate in student-facing form.

## On AI-generated code

This is a few hundred lines using well-documented libraries — squarely within what current models write
competently, and there is no reason to avoid using them.

The specific danger: **LLM-written orbital code looks right and silently uses the wrong frame.** It will
run, produce plausible numbers, and plot something believable. A student without programming experience
cannot catch that by reading it.

So the known-answer checks at every stage are not pedagogy garnish — they are the mechanism that makes
AI-assisted code safe here. Generate freely, verify against the physics every time.

## Compute budget, and why the stage ladder is also the compute ladder

The naive approach — a full year at 60 s cadence × a full sky map × path integration — is about
$5\times10^5 \times 10^3 \times 150 \approx 10^{11}$ field evaluations. Not feasible, and not necessary.

The sensible progression, which matches the student stages:

| Scope | Evaluations | Runtime |
|---|---|---|
| One epoch, one direction | ~150 | instant |
| One epoch, full sky map | ~150 k | seconds |
| One orbit, ~100 epochs | ~15 M | seconds to minutes, vectorised |
| Representative year (1 orbit per week) | ~800 M | minutes to hours; optimise then |

**Speed trick when it becomes necessary:** use a tilted dipole for broad scans — analytic, trivially
vectorised, and accurate to a few percent at these distances — and switch to full IGRF for final numbers.
Validating the dipole against IGRF is itself a useful check.

## Links

- part of [[../ALP]]
- what it computes: [[geomagnetic-integral]]
- cases: [[orbit-cases]]
- student view: [[../05-student/project-pathway]]
