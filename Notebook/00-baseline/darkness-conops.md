---
type: note
tags: [darkness, alp, baseline, conops]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# DarkNESS ConOps as inherited constraints

The ALP study does not get to design the spacecraft. It gets to choose **where to point, when**, inside
a ConOps that already exists. This note records that ConOps as a constraint set, so the pointing
optimisation in [[../02-mission-analysis/pointing-optimization]] optimises over the real feasible set
rather than an imagined one.

## The baseline mission, as published

Science operations run during **umbral passages** — the paper is explicit that eclipse observing reduces
solar background and gives stable thermal conditions (p. 4799). The baseline science phase is 187 days
between the 2026 equinoxes, targeting the Galactic Centre (Sagittarius) for the decaying-DM X-ray line,
with Cygnus (the solar apex) targeted year-round for the sub-GeV channel.

Attitude is a **two-axis constraint problem**, not a boresight problem. Every mode has a primary axis
(the science or comms direction) and a secondary axis that keeps radiators viewing deep space and away
from Earth (p. 4800). The cryocooler holds the MCM at 170 ± 5 K with a continuous power draw, so thermal
margin is a live constraint on attitude, not a design-time one.

## What this means for an ALP campaign

**The good news: this is a parasitic analysis.** The ALP signal is a diffuse surface brightness correlated
with the line-of-sight geomagnetic integral. Every science frame DarkNESS takes — GC, Cygnus, or blank
sky — carries a value of $(B_\perp L)^2$ determined by where the spacecraft was and where it was looking.
No dedicated observing time is strictly required to *start*. The analysis is a regression over frames that
are being taken anyway.

**The interesting news: pointing is free for one of the two channels.** See
[[../01-physics/alp-signal-chain]]. The universal continuous channel has an isotropic ALP flux, so the
sky direction is irrelevant and only the geomagnetic geometry matters — that makes it a pure mission-analysis
optimisation. The galactic monochromatic channel scales with the DM column density $S_\phi$, so it is a
joint optimisation over sky position *and* field geometry.

## Constraint set for the optimiser

| Constraint | Source | Status in the model |
|---|---|---|
| Umbra-only science | `DN-V` p. 4799 | **Baseline.** Flagged as a candidate to relax — see [[../decisions]] |
| Radiator secondary-axis constraint | `DN-V` p. 4800 | Must be modelled; it couples attitude to thermal |
| Earth limb avoidance | `ASSUME` | Angle TBD; bright-limb and albedo background rise sharply |
| Sun keep-out | `ASSUME` | Implied by radiator and window constraints, angle TBD |
| SAA exclusion | `EXT` + `DN-V` p. 4798 | Standard mask; costs duty cycle |
| Slew rate, settle time, momentum management | `DN-TBC` | Unknown — bounds how fast a scan law can move |
| Ground-station passes | `DN-V` p. 4799 | UHF command via ISU, S-band downlink; interrupts science |
| Downlink volume | `DN-TBC` | 105 Mb/day science vs 708 Mb/day capacity, unverified |

## The eclipse trade, stated early because it drives orbit choice

Umbra-only science interacts badly with one of the candidate orbits. A dawn/dusk SSO (LTAN 06:00/18:00)
has its orbital plane roughly normal to the Sun line and therefore spends most or all of the year with
**little or no eclipse**. A noon/midnight SSO (LTAN 12:00/00:00) maximises eclipse fraction. ISS-like sits
between, with a precessing beta angle that cycles eclipse fraction over ~60 days.

So the ranking under the published ConOps is roughly the inverse of what a power-systems engineer would
choose. This is developed in [[../02-mission-analysis/orbit-cases]].

## Links

- part of [[../ALP]]
- numbers: [[darkness-parameters]]
- consumes into: [[../02-mission-analysis/pointing-optimization]]
