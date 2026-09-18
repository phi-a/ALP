---
type: note
tags: [darkness, alp, mission-analysis, pointing, kinematics]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# The pointing system

Five words, in order, and every simulation run declares each one.
Physics of *where the field is* lives in [[pointing-optimization]];
this note is the machinery that turns a choice into a boresight per
sample.

## 1. Target — a direction per sample

`pointing.direction(spec, time, r, v, b)` → `(N, 3)` ECI unit vectors.

| Family | Specs | Source |
|---|---|---|
| inertial | `"gc"`, `"apex"`, `"ra,dec"` | astropy SkyCoord |
| solar-system | `"sun"`, `"moon"`, `"mars"`, … | astropy `get_body`, parallax from the spacecraft |
| orbit-based | `"zenith"`, `"nadir"`, `"velocity"`, `"orbit_normal"`, `"anti_sun"` (and `anti_` forms) | r, v, Sun |
| field-based | `"b_perp"` (across B, sky side), `"b_along"` (along B, sky side) | local B at the spacecraft |

The field-based rules are *local*. They are not the sky-wide optimum
(that is limb-grazing; see [[pointing-optimization]]) — they are the
cheap, executable versions of "look across" and "look along".

## 2. Mode — boresight target plus roll rule

`pointing.mode(primary, roll)`. The boresight (body +Z, `ASSUME`) goes
on the primary; the roll about it puts the radiator normal (body +Y,
`ASSUME`) toward `anti_earth` (zenith), `anti_sun`, or any target spec.
`pointing.desired_attitude(mode, …)` → body→ECI Rotation per sample.
Roll is analytic — the hint vector projected across the boresight — so
there is no optimiser and no search.

## 3. Schedule — condition → mode

`pointing.conditions(time, r, extra)` gives `umbra`, `sunlit`, `always`
and anything passed in (occulted, SAA, ground pass, …).
`pointing.select(rules, conds)` walks `[(condition, mode), …]`, first
match wins, and refuses to leave a sample unassigned.

```python
RULES = [("umbra", mode("gc", "anti_earth")),
         ("always", mode("anti_sun", "anti_earth"))]
```

Two fixed targets alternated, a field-tracking law in eclipse, a
ground-pass mode — all the same three lines.

## 4. Steering — chase the desired attitude at a fixed rate

`kinematics.steer(desired, t, rate_deg_s, settle_deg, mode_index)` →
commanded Rotations, pointing error in degrees, `slewing` flag. One
rule: each step rotates toward the desired attitude by at most
`rate × dt`. No wheels, no torques, no dynamics; the rate is a mission
input (`ASSUME 1.5°/s`, D11). A sample is `slewing` if it is still
behind the desired attitude or moved more than tracking within the same
mode requires — so a mode switch is flagged even when the slew finishes
inside one cadence step. `slewing` frames are excluded from science.

## 5. Boresight — into the state table

`kinematics.boresight(attitude)` → `(N, 3)`; `sim.state_table` takes it
as before and adds `mode` and `slewing` columns from the notebook.

## What this deliberately leaves out

- Attitude dynamics, wheel momentum, torques: `dynamics/attitude.py`
  when needed; the steering interface does not change.
- A pointing optimiser: the tiers in [[conops-physics-map]] are all
  expressible as rules; leverage-optimal schedules come later and will
  emit rules, not attitudes.
- Body geometry: `BORESIGHT_BODY` and `RADIATOR_BODY` are placeholders
  until Q4.

## Links

- part of [[../ALP]]
- physics of the choice: [[pointing-optimization]]
- constraints: [[../00-baseline/darkness-conops]]
- code: [[tooling]]
