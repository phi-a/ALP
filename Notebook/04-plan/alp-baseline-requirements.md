---
type: requirements
tags: [darkness, alp, requirements, baseline]
created: 2026-09-23
updated: 2026-09-23
status: active
---

# ALP baseline requirements

## Scope

These requirements govern the ALP study only: the geomagnetic
ALP–photon detection channel, its modelling, and the DarkNESS mission
analysis that selects an observing ConOps for it. They follow the
project statement in [[project-charter]]:

> Using the DarkNESS platform, what observing ConOps maximises the
> identifiable geomagnetic ALP–photon conversion signal against
> particle and diffuse X-ray backgrounds, and what does that ConOps
> require of the mission?

Out of scope: the DarkNESS platform design, the sterile-neutrino
program, and the coupling limit (a conditional follow-on, charter
§Research question).

## Form

Each requirement is one sentence: *The ⟨work product⟩ shall ⟨verb⟩
⟨object⟩ ⟨qualifier⟩.* One obligation per line, no "and", no "or".
The subject is always a work product, never a person. Each carries a
verification method and one status:

| Status | Meaning |
|---|---|
| **Met** | verified; evidence cited |
| **Open** | not yet verified |
| **Gated** | verification waits on a named decision gate |
| **Retired** | withdrawn by a decision; kept for traceability |

Verification methods: **T** test in `tests/`, **A** analysis recorded
in `Notebook/`, **I** inspection of code or note, **R** independent
review.

Changing a requirement is a dated entry in [[../decisions]]; the
status column here is updated with the evidence pointer.

## CH — Detection channel

| ID | Requirement | V | Status |
|---|---|---|---|
| ALP-CH-01 | The source model shall represent the incident ALP intensity as the two-body decay $\chi\to aa$ of a non-relativistic dark-matter parent. | I | **Met** — [[../01-physics/detection-channel-derivation-contract]] §Physical hypothesis |
| ALP-CH-02 | The source model shall include the Milky Way line component at $E_0 = m_\chi/2$. | T | **Open** |
| ALP-CH-03 | The source model shall include the extragalactic continuum component with support only at $E \le E_0$. | T | **Open** |
| ALP-CH-04 | The source model shall derive the Milky Way component from the same parent parameters $(f_\chi, \tau_\chi, \mathcal B_{aa})$ as the extragalactic component. | A | **Open** — D15 |
| ALP-CH-05 | The Milky Way component shall scale with the dark-matter column density $D_\chi(l,b)$ along the boresight. | T | **Met** — `test_source.TestHalo`, `d_gevcm2` |
| ALP-CH-06 | The source model shall reproduce one published benchmark spectrum without a fitted scale factor. | A | **Gated** — D16 |
| ALP-CH-07 | The conversion model shall integrate the signed transverse field vector along each ray. | T | **Met** — `test_reversal_shows_a_dip` |
| ALP-CH-08 | The conversion model shall carry the phase $q = m_a^2/2E$ along each ray. | T | **Met** — `test_phase_reduces_amplitude` |
| ALP-CH-09 | The conversion model shall reproduce the analytic $\mathrm{sinc}^2$ result for a uniform field with constant phase. | T | **Open** |
| ALP-CH-10 | The conversion model shall reproduce the dipole closed forms at zenith to 1 %. | T | **Met** — `test_zenith_and_nadir_closed_forms` |
| ALP-CH-11 | The conversion model shall terminate an occulted ray at the Earth surface. | T | **Met** — `test_zenith_and_nadir_closed_forms`, `s_km` end |
| ALP-CH-12 | The conversion model shall change by less than 2 % when the outer radius is doubled from 10 Earth radii. | T | **Met** — `test_outer_radius_converges` |
| ALP-CH-13 | The conversion model shall include the plasma frequency term in the phase. | T | **Open** |
| ALP-CH-14 | The conversion model shall take the internal geomagnetic field as a separable input from any external field. | I | **Open** |
| ALP-CH-15 | The conversion kernel shall be averaged over the 20° full-cone aperture. | T | **Met** — `test_fov_hairline_cone_is_the_boresight`, [[../2026-09-23-fov-field-integral]] |
| ALP-CH-16 | The aperture average shall converge to 1 % under one ring refinement. | A | **Open** |
| ALP-CH-17 | The aperture average shall recover the boresight kernel as the cone half-angle tends to zero. | T | **Met** — `test_cone_average_recovers_the_boresight_in_a_smooth_field` |
| ALP-CH-18 | The source model shall include the primordial cosmic ALP background as an isotropic component with a normalisation independent of $\Theta$. | T | **Retired** — D26 |
| ALP-CH-19 | The cosmic ALP background spectrum shall follow the Conlon–Marsh thermal-like form with the mean energy as a declared parameter. | I | **Retired** — D26 |
| ALP-CH-20 | The cosmic ALP background normalisation shall respect the declared $\Delta N_{\rm eff}$ bound. | A | **Retired** — D26 |
| ALP-CH-21 | The forecast shall report the fraction of the cosmic ALP background spectrum falling inside the 1–10 keV science band. | A | **Retired** — D26 |
| ALP-CH-22 | The forecast shall report the spectral separability of the cosmic ALP background from the extragalactic continuum inside the science band. | A | **Retired** — D26 |

ALP-CH-18 to ALP-CH-22 are retired (D26): at the CAST coupling limit
the geomagnetically converted cosmic ALP background is at most
$10^{-14}$ of the diffuse X-ray background in 1–10 keV. The same
conversion probability applies to every isotropic source, which sets
the bar the extragalactic continuum must clear at the viability gate.

## MD — Counts model

| ID | Requirement | V | Status |
|---|---|---|---|
| ALP-MD-01 | The counts model shall express the signal expectation per time interval per energy bin as the integral of $I_a\,P_{a\to\gamma}\,A\,T\,\mathrm{QE}\,\epsilon\,R$ over the triple $(t, \Omega, E)$. | R | **Open** — contract §3 |
| ALP-MD-02 | The signal expectation shall factor as $\Theta\,k_{ij}$ with $\Theta = g_{a\gamma\gamma}^2 f_\chi\mathcal B_{aa}/\tau_\chi$. | A | **Open** |
| ALP-MD-03 | The counts model shall recover the published grasp for an isotropic constant-brightness source. | T | **Open** |
| ALP-MD-04 | The counts model shall conserve counts through energy redistribution for a monochromatic input. | T | **Open** |
| ALP-MD-05 | The counts model shall apply the masking loss exactly once. | T | **Open** |
| ALP-MD-06 | The counts model shall apply the live-time loss exactly once. | T | **Open** |
| ALP-MD-07 | The counts model shall carry the 20° full cone (half-angle 10°, $\Omega = 0.0955$ sr) as the aperture acceptance. | I | **Met** — `half_angle_deg=10.0` default; [[../00-baseline/darkness-parameters]] |
| ALP-MD-08 | The counts model shall distinguish geometric area from effective collecting area. | I | **Open** — 12 cm² vs 8 cm² × 0.20 unreconciled |

## MA — Mission analysis

| ID | Requirement | V | Status |
|---|---|---|---|
| ALP-MA-01 | The state table shall record one sample per cadence step over the run duration. | T | **Met** — `test_duty_cycle` (144 at 600 s) |
| ALP-MA-02 | The state table shall record, per sample, the geometry fields of Table G. | I | **Met** — `sim.state_table` |
| ALP-MA-03 | The state table shall record, per sample, the background proxy fields of Table B. | I | **Open** — functions exist, columns absent |
| ALP-MA-04 | Repeated runs with identical inputs shall produce identical kernel values. | T | **Met** — `test_run_is_deterministic` |
| ALP-MA-05 | The state table shall record the aperture-averaged kernel beside the boresight kernel. | T | **Met** — `k_fov_t2m2`, `k_t2m2` |
| ALP-MA-06 | The nuisance model shall include cutoff rigidity as a regressor. | A | **Open** |
| ALP-MA-07 | The nuisance model shall include limb angle as a regressor. | A | **Open** — Q22 |
| ALP-MA-08 | The nuisance model shall include Galactic ridge brightness as a regressor. | A | **Open** |
| ALP-MA-09 | The forecast shall report the correlation of the aperture-averaged kernel against each regressor for the evaluated schedule. | T | **Met** for the boresight kernel — `test_background_confounding` |
| ALP-MA-10 | The forecast shall report the conversion information remaining after nuisance projection. | A | **Open** — contract §4 |
| ALP-MA-11 | The schedule comparison shall evaluate one feasible high-conversion schedule against the nominal Galactic Centre schedule. | A | **Open** |
| ALP-MA-12 | The schedule comparison shall evaluate one feasible low-conversion schedule against the nominal Galactic Centre schedule. | A | **Open** |
| ALP-MA-13 | The schedule comparison shall exclude slewing samples from science exposure. | T | **Met** — `sky` mask in `test_scenario_regression` |
| ALP-MA-14 | The schedule model shall offer umbra-only science as a selectable rule. | T | **Met** — `pointing.conditions`, D5 |
| ALP-MA-15 | The schedule model shall enforce a Sun keep-out angle on the boresight. | T | **Open** — `feasible` exists, untested, unapplied |
| ALP-MA-16 | The schedule model shall enforce an Earth-limb keep-out angle on the boresight. | T | **Open** — `feasible` exists, untested, unapplied |
| ALP-MA-17 | The schedule model shall exclude SAA passages from science exposure. | T | **Open** |
| ALP-MA-18 | The schedule model shall limit the commanded slew rate to the declared value. | T | **Met** — `test_steering_never_exceeds_the_rate` (1.5°/s `ASSUME`) |
| ALP-MA-19 | The extended run shall report the spread of the figure of merit over the initial orbital phase. | A | **Open** |
| ALP-MA-20 | The ConOps deliverable shall assign each mission constraint one provenance label from {published, adopted, unresolved}. | I | **Met** — [[../00-baseline/darkness-conops]] constraint table |
| ALP-MA-21 | The ConOps deliverable shall state the gain of the selected schedule over the nominal Galactic Centre pointing as a ratio of residual conversion information. | A | **Open** — charter sub-question 2 |
| ALP-MA-22 | The ConOps deliverable shall state each platform requirement that the selected schedule imposes. | I | **Open** — charter sub-question 1 |
| ALP-MA-23 | The ConOps deliverable shall state the background monitoring needed for the signal to remain identifiable. | A | **Open** — charter sub-question 4 |

## PR — Formal

| ID | Requirement | V | Status |
|---|---|---|---|
| ALP-PR-01 | Every public library function shall have a docstring. | T | **Met** — `test_every_function_has_a_docstring` |
| ALP-PR-02 | Every public library function shall appear in the generated API reference. | T | **Met** — `test_every_public_name_appears` |
| ALP-PR-03 | Every public library function shall have a known-answer test. | I | **Met** — CLAUDE.md rule; `tests/` |
| ALP-PR-04 | The library shall import only numpy, scipy, astropy, matplotlib beyond the standard library. | I | **Met** — `pyproject.toml`, D21 |
| ALP-PR-05 | A pinned scenario answer shall change only through a dated decision-log entry. | I | **Met** — `test_scenario_regression` docstring, D22 |
| ALP-PR-06 | The viability gate shall receive one disposition from {Continue, Revise, Redirect} before any absolute sensitivity is reported. | I | **Gated** — D16 |
| ALP-PR-07 | Every reported sensitivity number shall carry its level in the result hierarchy of contract §4. | I | **Open** |
| ALP-PR-08 | Every mission conclusion shall cite the state-table run that produced it. | I | **Open** |

## Table G — geometry fields

`t_s`, `x_km y_km z_km`, `lat_deg lon_deg alt_km`, `maglat_deg`,
`cutoff_gv`, `limb_deg`, `sun_deg`, `umbra`, `occulted`,
`l_deg b_deg`, `amp_tm`, `k_t2m2`, `k_fov_t2m2`, `fov_occ_frac`,
`d_gevcm2`, `d_fov_gevcm2`, `dk_fov_gevcm2_t2m2`.

## Table B — background proxy fields

`grxe`, `nxb_rel`, `bright_src_mcrab`, `saa`.

## Tally

| Group | Met | Open | Gated | Retired |
|---|---:|---:|---:|---:|
| CH | 9 | 7 | 1 | 5 |
| MD | 1 | 7 | 0 | 0 |
| MA | 9 | 14 | 0 | 0 |
| PR | 5 | 2 | 1 | 0 |
| **Total** | **24** | **30** | **2** | **5** |

## Links

- part of [[../ALP]]
- frame: [[project-charter]]
- derivation checks these formalise: [[../01-physics/detection-channel-derivation-contract]]
- work package: [[mission-identifiability-work-package]]
- decisions: [[../decisions]]
