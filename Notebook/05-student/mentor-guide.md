---
type: note
tags: [darkness, alp, student, mentoring]
created: 2026-07-28
updated: 2026-09-17
status: active
audience: mentor
---

# Mentor guide

Companion to [[project-pathway]]. That one is written for the student; this one is for running it.

## The design principle behind the stage structure

Each stage has a **known answer** attached — 94-minute orbital period, the South Atlantic Anomaly showing
up in the right place, ~100 T m from a hand calculation, Yamamoto's published limit reproduced. This is
deliberate and it is doing most of the mentoring work for you.

A student with weak programming experience cannot tell the difference between "my code works" and "my code
runs." Known answers close that gap without you having to read their code. When they say "I'm stuck," the
first question is always *which check is failing*, and that usually localises the problem to one stage.

It also means they can work between meetings without being blocked on you.

## Where the difficulty actually is

Not where it looks. Ranked by how much trouble it causes in practice:

1. **Coordinate frames (Stage 1–2).** Inertial vs Earth-fixed vs geodetic lat/lon/alt. This will cost more
   time than the physics. It is worth being heavy-handed here: make them write down which frame every array
   is in, in a comment, every time. The South Atlantic Anomaly check in Stage 2 catches most frame errors,
   which is why it's there.
2. **The line integral (Stage 3).** Conceptually simple, fiddly in practice. Two specific traps: taking
   absolute values inside the sum (removes real cancellation, inflates the answer), and stopping the
   integration too early.
3. **Reproducing the published limit (Stage 5).** Where scope creep dies. If it does not reproduce, the
   temptation is to move on anyway. Do not let that happen — it is the gate that makes the final number
   worth anything.

The physics itself is not the hard part. Stage 0 is genuinely approachable for an undergrad.

## Meeting rhythm

Weekly, 30 minutes, same three questions:

1. Show me the figure from where you are.
2. What number did you check it against?
3. What is the one thing blocking you?

If there is no figure, the meeting is about why not — do not let it become a status discussion. The figure
is the unit of progress, and every stage produces exactly one.

## Diagnosing "I'm stuck"

Two failure modes, different responses:

- **Stuck on physics** — they cannot say what the number should be. Response: work the hand calculation
  with them, before any code. Stage 3's 100 T m estimate is the model for this; it takes ten minutes on
  paper and it makes the coding tractable.
- **Stuck on code** — they know what they want and can't get it. Response: shrink the problem. One time
  step instead of a day. One direction instead of a sky map. Print intermediate values. Most students in
  this position are debugging at full scale.

The two-hour rule in the student doc exists so they don't burn a week silently.

## What to hold back, and when to introduce it

The intellectual core of this project — that the measurement is a *correlation* and what matters is having
both strong- and weak-field pointings under matched conditions — is introduced in Stage 4 in plain language
("control group"). That is the right time: they have a sky map in front of them and the idea lands
concretely.

Introducing it earlier turns into an abstract statistics lecture. Introducing it later means Stage 4 gets
built toward the wrong objective (maximise the field) and has to be redone.

The full version — Fisher information, leverage, and the fact that particle background correlates with
geomagnetic position and is the dominant confounder — lives in
[[../02-mission-analysis/pointing-optimization]]. That is yours, not theirs, unless they turn out to be
strong and want it.

## Scope control

The student pathway deliberately excludes: automatic optimisation, background modelling from scratch, the
external field model, atmospheric absorption, thermal and attitude constraints. All are real and all are in
the research plan. None belong in a first pass.

If the student is moving fast, the right extension is **not** to add physics. It is to add *cases* — run
Stage 4 for the other two orbits ([[../02-mission-analysis/orbit-cases]]). Same code, three times the
result, and it directly feeds the actual deliverable.

## Honest expectation setting

Tell them the expected answer early — a factor of three or four, no extension in mass reach. Two reasons:
it prevents the disappointment of "we didn't find the axion," and it makes an anomalously good result
trigger suspicion rather than celebration.

Also worth saying out loud once: reproducing a known result *is* research output. Stage 5's Suzaku
reproduction is a real contribution to the project's credibility, not a warm-up exercise.

## Blocking items that are yours, not theirs

From [[../open-questions]]: Q1 (is the 20° FOV a full cone or a half-angle) and Q2 (why the existing chain
uses 8 cm² and 20% against a published 12 cm² and ~50% masking). Both scale the final number linearly.
Both are one email. Neither should be the student's problem, and Stage 5 will produce a wrong number
without them.

## Reference implementations exist (2026-09-17)

Stages 1–4 are covered by the library in `src/darknessalp/` (numpy,
scipy, astropy; topic folders; known-answer tests) and the run notebook
`jupyter/main_sequence.ipynb`. See [[../02-mission-analysis/tooling]].
The student drives the notebook and writes little code; the fifteen-line
orbit and the hand integral in Stages 1 and 3 are still worth doing once
on paper or in a scratch cell, then compared with the library. The tests
are the answer key: `python -m unittest discover -s tests`.

One check changed: the Stage 4 intuition "smallest along the field lines"
is only true at high magnetic latitude. The corrected version is in
[[project-pathway]] and the numbers are in
[[../02-mission-analysis/pointing-optimization]].

## Links

- student version: [[project-pathway]]
- tools: [[../02-mission-analysis/tooling]]
- full research plan: [[../04-plan/research-plan]]
- home: [[../ALP]]
