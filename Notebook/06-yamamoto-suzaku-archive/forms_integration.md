---
title: FORMS Integration Decision
status: accepted
updated: 2026-07-30
---

# FORMS Integration Decision

## Decision

Use FORMS as the mission-analysis engine for the DarkNESS ALP feasibility
study. Keep the ALP conversion physics, Yamamoto reproduction, instrument
response, background inference, and projected-limit calculation in this
repository.

The interface is a time-indexed state table:

```text
FORMS orbit + attitude + environment
    -> ALP mission-state adapter
    -> boresight/FOV geometry + line-of-sight field integral
    -> signal and background regressors
    -> likelihood and projected limit
```

This boundary makes the journal contribution reproducible without turning
FORMS into a particle-physics package or duplicating its astrodynamics code.

## Extension and ownership rule

Classify each missing capability by where it is reusable:

1. A general mission-analysis model belongs in FORMS as a validated topic
   brick. Examples include an Earth-limb geometry model, radiation-environment
   proxy, instrument keep-out evaluator, or a generally useful observation
   opportunity model.
2. A mission-specific calculation that combines existing FORMS state belongs
   in the DarkNESS workspace as a routine. A routine takes the `forms` handle,
   reads only supported mission state, and may publish derived variables back
   to the handle for recording, events, or scheduling.
3. Astrophysical signal, detector inference, and particle-physics calculations
   belong in ALP modules. A thin routine may call those modules to expose a
   scalar such as the FOV-averaged conversion regressor, but the scientific
   implementation and tests remain independent of FORMS.

This gives FORMS a clean path to grow when the study identifies a genuinely
general modeling gap, while preventing DarkNESS-specific assumptions from
entering the mission engine.

## Capabilities to import

Use the supported `forms` handle for:

- LEO initialization and propagation, including TLE/SGP4 and higher-fidelity
  force-model cases where required.
- GCRS/ITRF and geodetic frame transformations.
- spacecraft attitude and commanded pointing state.
- Sun and Moon geometry, illumination, and eclipse windows.
- IGRF-13 magnetic field at the spacecraft, including `BGCRS` in Tesla.
- time-indexed variable recording and mission event summaries.

The current FORMS SDK exposes the package through `import forms` and requires
Python 3.10 or newer. Its base dependencies are NumPy, PyYAML, and Matplotlib.
The slim distribution is `forms-sdk`; it and the full `forms` distribution
provide the same import name and must not be installed together.

## Capabilities retained here

The ALP repository owns:

- reconstruction of Suzaku orbit and attitude samples from archived files;
- ray generation over the DarkNESS field of view;
- integration of the transverse magnetic field beyond the spacecraft along
  each ray;
- ALP coherence and conversion probability;
- detector response, backgrounds, scheduling objective, likelihood, and
  projected coupling limit;
- comparison with Yamamoto Figure 7.

ALP modules should expose ordinary typed Python functions that accept explicit
state and model parameters. FORMS routines are adapters around those functions,
not their implementation home. This permits unit testing the astrophysics
without propagating a mission and permits the same functions to operate on
archived Suzaku states.

FORMS currently publishes the magnetic field at the spacecraft. The ALP
observable instead needs an integral along a ray through the magnetosphere.
Therefore `BGCRS` is a useful frame/unit validation point, not a replacement
for the line-of-sight integration kernel.

## Dependency policy

For analysis development, install the local SDK checkout into a dedicated ALP
virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e C:\Users\phial\Documents\Python\forms\python\sdk
```

Before a reproducible release, replace the editable dependency with an
immutable FORMS commit pin and record that commit in the environment lock or
provenance metadata. Do not depend on internal paths such as
`forms.core.forms`; client code should begin with `import forms` and use the
published handle and catalog.

## Validation gates

1. Confirm the ALP environment imports `forms` and records the FORMS version
   and source revision.
2. Reproduce a simple LEO trajectory and compare position, eclipse state, and
   field units against an independent case.
3. At each spacecraft sample, compare the existing ALP IGRF result with FORMS
   `BGCRS` after making epoch, frame, and units identical.
4. Validate boresight construction from the FORMS attitude convention using
   known nadir, zenith, velocity, and fixed-inertial test cases.
5. Keep the Suzaku reconstruction independent of FORMS propagation so the
   Yamamoto validation uses archived spacecraft states rather than a synthetic
   replacement.

## Immediate implementation

The first adapter should emit only the fields needed for Yamamoto validation
and later DarkNESS trades:

- epoch and elapsed time;
- GCRS position and velocity;
- geodetic latitude, longitude, and altitude;
- inertial boresight and FOV convention;
- eclipse/illumination and Earth-limb angle;
- Sun and Moon separation;
- local and GCRS magnetic field;
- orbit/environment quality flags;
- provenance for FORMS version, field model, frame data, and source orbit.

The background model and optimized scheduler remain downstream work. They
should consume this table rather than call FORMS directly.

## Initial routine boundary

The first DarkNESS routine should:

1. read epoch, spacecraft position, attitude/boresight, illumination, and
   environmental variables from the `forms` handle;
2. construct an immutable ALP mission-state input;
3. call an ALP-owned FOV and line-of-sight integration function;
4. publish compact outputs such as `alp_bperp_l2_mean`,
   `alp_bperp_l2_variance`, valid-ray fraction, limb margin, and model-quality
   flags; and
5. leave spectral prediction and likelihood evaluation to an offline ALP
   analysis consuming the recorded state table.

If implementing this routine reveals a missing frame, environment, geometry,
or event model that is not ALP-specific, promote that capability to a FORMS
brick with a published reference, validation data, and a stable handle surface.
