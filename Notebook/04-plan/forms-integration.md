---
type: decision
tags: [darkness, alp, forms, interface]
created: 2026-07-30
updated: 2026-09-08
status: accepted
---

# FORMS integration

## Decision

FORMS provides orbit propagation, frames, attitude state, illumination,
eclipse, limb geometry, geomagnetic state, environment variables, and mission
event recording. The ALP package provides the line-of-sight conversion kernel,
field-of-view integration, source model, detector response, background
inference, scheduling metric, and sensitivity calculation.

A time-indexed state table defines the interface:

```text
FORMS orbit, attitude, and environment
    -> DarkNESS mission-state adapter
    -> ALP conversion and background regressors
    -> schedule comparison and likelihood
```

General mission-analysis capability belongs in FORMS. DarkNESS-specific state
assembly belongs in the DarkNESS analysis. Particle physics and inference
remain in `Python/darkmatter/ALP`.

## Implementation record

The detailed interface, dependency policy, schema fields, and validation gates
are maintained with the code in
`Python/darkmatter/ALP/docs/forms_integration.md`.

## Current use

[[next-step]] requires FORMS to generate the reference orbit and constrained
boresight state. The ALP repository consumes that state and produces the
conversion kernel and identifiability diagnostics. The Notebook records the
interpretation and resulting project decision.

## Links

- charter: [[project-charter]]
- current work: [[next-step]]
- field integral: [[../02-mission-analysis/geomagnetic-integral]]
- decisions: [[../decisions]]
