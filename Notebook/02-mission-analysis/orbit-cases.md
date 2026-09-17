---
type: note
tags: [darkness, alp, mission-analysis, orbit]
created: 2026-07-28
updated: 2026-07-28
status: active
---

# Orbit cases

The published orbit is "~500 km SSO **or** ISS-like mid-inclination, determined at manifest" (`DN-V`
p. 4799). So the study cannot assume one — it has to carry the cases and report a Pareto answer.

## The three cases

| Case | Altitude | Inclination | LTAN | Status |
|---|---|---|---|---|
| **ISS-like** | ~400–420 km | 51.6° | n/a (precessing) | Baseline case 1 |
| **SSO noon/midnight** | ~500 km | ~97.4° | 12:00 / 00:00 | Baseline case 2 |
| **SSO dawn/dusk** | ~500 km | ~97.4° | 06:00 / 18:00 | Optional third case |

## What differs, physically

**Geomagnetic latitude coverage.** SSO is polar, so it sweeps the full range of magnetic latitudes every
orbit; ISS-like is confined to ±51.6° geographic. Field strength and direction — and therefore both the
magnitude and the *variance* of $B_\perp L$ — differ substantially. Since the analysis is a regression on
$(B_\perp L)^2$, the **spread** matters as much as the mean (see [[pointing-optimization]]), and polar
coverage plausibly wins on spread. That is a hypothesis the simulation should test, not an assumption.

**Particle background.** The same polar coverage that gives field diversity costs background: geomagnetic
cutoff rigidity falls toward the poles, so cosmic-ray access rises. SSO passes through the polar horns
every orbit. ISS-like avoids the horns but has substantial SAA exposure. Background enters $g_{\min}$ at
the 1/4 power while $B_\perp L$ enters linearly, so **field geometry should win this trade** — but the
duty-cycle loss from SAA/horn masking is a direct multiplier on exposure and needs to be counted.

**Eclipse fraction, which is the sharp one.** Science is umbra-only in the published ConOps
([[../00-baseline/darkness-conops]]):

- *Noon/midnight SSO* — orbit plane contains the Sun line, maximum eclipse (~35 % per orbit), stable
  year-round. **Best for umbra-only science.**
- *ISS-like* — beta angle precesses on a ~60-day cycle; eclipse fraction cycles from ~40 % down to near
  zero at high beta. Seasonal, plannable.
- *Dawn/dusk SSO* — orbit plane roughly normal to the Sun line, **little or no eclipse for much of the
  year**. Near-continuous power, which is why it is attractive to a power budget, and close to useless for
  umbra-only observing.

If dawn/dusk is manifested, the umbra-only constraint has to be relaxed or the ALP campaign loses most of
its duty cycle. That makes "is umbra-only actually required for *this* analysis?" a live question rather
than an academic one — logged in [[../decisions]].

## Altitude

ISS-like sits ~100 km lower, which puts the spacecraft marginally deeper in the field — but the integral
runs out to several $R_E$, so the endpoint dominates and the altitude difference is a small effect on
$B_\perp L$. It matters more for drag lifetime and for trapped-particle exposure. Do not over-weight it.

## What the study must produce per case

For each of the three, over a representative year:

1. Distribution of achievable $(B_\perp L)^2$ — mean, spread, and the accessible upper tail
2. Duty cycle after umbra, SAA, limb, Sun, and radiator constraints
3. Resulting projected $g_{\min}$ under a fixed analysis
4. Sensitivity of the answer to the umbra-only assumption

The deliverable is a ranking with the reasoning attached, so that whichever orbit the manifest assigns,
the pointing scheme for it already exists.

## Links

- part of [[../ALP]]
- constraints: [[../00-baseline/darkness-conops]]
- field model: [[geomagnetic-integral]]
- objective: [[pointing-optimization]]
