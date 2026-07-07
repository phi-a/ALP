# ALP Problem Research Notes

Living reference for the ALP mission analysis, simulation design, and
optimization work.

Last updated: 2026-07-07

## Purpose

This document is the shared record for the ALP problem: what we believe, what we
have tested, what is still uncertain, and how the simulation should evolve. Keep
the mission notebook focused on executable analysis; keep the reasoning,
assumptions, references, and decisions here.

## Current Focus

- Understand axion-like particles (ALPs), their candidate production channels,
  and observable signal models.
- Build toward a FORMS-based mission simulation for a LEO dark matter search.
- Model the reverse Primakoff effect at the level needed for mission trades.
- Track assumptions, references, equations, and decisions as the work changes.
- Develop an optimization workflow for orbit, duty cycle, magnetic exposure,
  observing geometry, and operational constraints.

## Core Problem Statement

We want to evaluate whether a spacecraft mission concept can improve sensitivity
to ALP-related signatures by exploiting orbital access to geomagnetic and
space-environment conditions. The first simulation target is a transparent
pipeline that connects orbit choices to exposure metrics, then grows into a
physics-informed signal and optimization model.

## Working Mission Questions

- Which orbital regimes maximize useful magnetic-field exposure?
- How do eclipse, attitude, ground contact, and operations constraints change
  the available observing time?
- What signal proxy should be used before the full ALP response model is ready?
- Which parameters are design variables, which are environmental variables, and
  which are fixed assumptions?
- What objective function best reflects the science value of a candidate orbit?

## Initial Simulation Scope

The first FORMS mission notebook should stay modest and inspectable:

- Create a FORMS handle with `forms.FORMS()`.
- Use `api_search` and `book_ai` to identify the correct FORMS calls before
  building mission logic.
- Define a baseline LEO orbit.
- Propagate over a representative time span.
- Record orbit state, altitude, eclipse state, and magnetic-field-related
  quantities if available from FORMS.
- Produce simple plots and summary tables into `outputs/`.

## Candidate Design Variables

- Altitude or semi-major axis.
- Inclination.
- RAAN and local time if sun-synchronous options become relevant.
- Eccentricity for non-circular trades.
- Propagation duration and step size.
- Observation duty-cycle constraints.
- Field-of-view or pointing constraints, once an instrument model exists.

## Candidate Metrics

- Integrated magnetic-field exposure along the orbit.
- Time spent above a magnetic-field threshold.
- Eclipse or sunlight duty cycle.
- Fraction of orbit satisfying operations constraints.
- Combined science utility score for optimization sweeps.

## FORMS Investigation Log

Use this section to record useful FORMS documentation discoveries. For each
entry, include the query, the symbol or doc page found, and the reason it matters.

| Date | Query | FORMS result | Notes |
| --- | --- | --- | --- |
| 2026-07-07 | `magnetic field` | TBD | Find the preferred geomagnetic model or variable. |
| 2026-07-07 | `eclipse` | TBD | Confirm eclipse variables and summary APIs. |
| 2026-07-07 | `sun synchronous` | TBD | Check whether sun-sync orbit design is built in. |
| 2026-07-07 | `set propagator rk4` | `Propagator.set_type` supports `sgp4`, `rk45`, and `kepler`; `RK45Integrator` is Dormand-Prince RK4(5). | Use fixed-step `rk45` with adaptive mode disabled for the first point-mass numerical propagation. |

## Assumptions

- The installed `forms` package is treated as an external dependency and is not
  edited in this workspace.
- Mission scripts and notebooks live in `missions/`.
- Reusable calculations live in `routines/`.
- Generated results live in `outputs/`.
- Early signal metrics may be proxies until the ALP response model is defined.

## References

- Yamamoto 2020 JCAP paper in `docs/`.
- FORMS SDK catalog via `f.api_search(...)`.
- FORMS authored book via `f.book_search(...)` and `f.book_ai(...)`.

## Decisions

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-07-07 | Use `docs/alp_research_notes.md` as the living ALP reference. | Keeps research context separate from executable mission code. |
| 2026-07-07 | Start the executable ALP analysis in `missions/alp_simulation.ipynb`. | Matches workspace convention that full simulations belong in `missions/`. |
| 2026-07-07 | Configure the first LEO mission as point-mass gravity with fixed-step `rk45` and no environmental perturbation forces. | FORMS does not expose a separate `rk4` propagator type; this gives a simple numerical baseline without drag, SRP, J2, or third bodies. |

## Open Questions

- What is the minimum acceptable ALP signal model for the first optimization
  pass?
- Which geomagnetic model should be considered baseline?
- What orbit classes should be compared first?
- What mission constraints are mandatory versus nice-to-have?
- What outputs should become stable artifacts for later comparison?

## Change Log

- 2026-07-07: Converted the short note into a structured living reference and
  created the first mission notebook companion.

## Definitions/note :
- Earth limb angle = how close the detector boresight is to the visible edge of Earth
- earth occultation- due to LEO, Earth cud hinder with cubeSAT POV, we need moderately above limb: good balance of magnetic feild vs background 
- signal to noise ratio
- signal_proxy = B_perp**2 * L_eff**2
- background_total = (
    cosmic_background
    + limb_background
    + particle_background
    + detector_background
)
- snr_score = signal_proxy / np.sqrt(background_total) : SIMPLIFIED SNR IF signal_proxy << background_total
## Plot 1: Ground Track
x-axis: longitude
y-axis: latitude
purpose: verify LEO orbit simulation
## Plot 2: Valid Pointing Directions
x-axis: pointing azimuth
y-axis: pointing elevation or Earth limb angle
purpose: show which attitudes are blocked by Earth and which are valid(minimum lim angle to target)
## Plot 3: Signal Proxy vs Earth Limb Angle
x-axis: angle above Earth limb
y-axis: (B_\perp^2 L_{\text{eff}}^2)
purpose: show where ALP conversion geometry is strongest
## Plot 4: Background vs Earth Limb Angle
x-axis: angle above Earth limb
y-axis: total background proxy
purpose: show how background increases near Earth
## Plot 5: SNR Score vs Earth Limb Angle
x-axis: angle above Earth limb
y-axis: signal proxy divided by square root of background
purpose: identify the best attitude region
## Plot 6: Best SNR Score Over Orbit
x-axis: time since orbit start
y-axis: maximum SNR score
purpose: identify best observation windows (location in orbit)--- doubts about this
Strategy A: Fixed pointing angle , Strategy B: Optimized pointing angle at every time
## Plot 7: Best Pointing Angle Over Orbwait buit
x-axis: time since orbit start
y-axis: best Earth limb angle or best detector pointing direction
purpose: understand how the optimal attitude changes along the orbit