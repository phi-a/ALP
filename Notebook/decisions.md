---
type: note
tags: [darkness, alp, decisions]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# Decision log

Append-only. Each entry: what was decided, why, and what would reverse it. Reversals get a new entry
rather than an edit.

---

## D1 — The DarkNESS-precise line is kept separate from the general SmallSat survey

**2026-07-28.** [[darkness_alp]] surveys the whole LEO-SmallSat ALP mission class (SDD, GPD, MiXO
concepts; HaloSat, MinXSS, ASTERIA, SSAXI heritage) and treats DarkNESS as one option among several. That
report stays as prior art. Everything under `00-` through `04-` is DarkNESS-specific, with every parameter
traceable to [[00-baseline/darkness-parameters]] and provenance-tagged.

**Why:** a projected sensitivity curve is only as credible as the weakest parameter in it. Mixing
"DarkNESS actually has 12 cm²" with "a hypothetical SDD payload might have X" is how a mission study
quietly becomes fiction.

**Reversed if:** the mission concept changes enough that DarkNESS is no longer the target platform.

---

## D2 — Galactic Centre pointing is not required

**2026-07-28.** The ALP analysis does not inherit the GC-pointing requirement of the primary science.

**Why:** Channel A's ALP flux is isotropic, so pointing enters only through $(B_\perp L)^2$. This frees the
boresight for a pure mission-analysis optimisation and is what makes the pointing study the research
element. Channel B does scale with $S_\phi$ and still benefits from GC pointing, so both are carried.

**Reversed if:** Channel B turns out to dominate the achievable sensitivity, which would re-couple sky
position to the objective.

---

## D3 — Channel A (universal continuous) is primary

**2026-07-28.** Effort goes to the isotropic channel first.

**Why:** it is where mission analysis has leverage — free pointing, pure geomagnetic optimisation. Channel
B is scientifically attractive (a line is a better discriminant, and the skipper-CCD's Fano-limited
resolution suits it) but the pointing problem there is partly constrained by astrophysics.

**Reversed if:** the line-vs-continuum background discrimination advantage turns out to outweigh the
pointing freedom. Worth a quantitative check rather than assumption.

---

## D4 — Three orbit cases carried, no baseline chosen

**2026-07-28.** ISS-like, SSO noon/midnight, SSO dawn/dusk all modelled. Dawn/dusk included despite being
the worst fit to umbra-only observing, precisely because that conflict needs to be quantified rather than
asserted.

**Why:** the orbit is set at manifest (`DN-V` p. 4799) and is not ours to choose. Delivering a ranking with
a ready pointing scheme for each is more useful than optimising the wrong one.

**Reversed if:** the manifest fixes the orbit before the study completes — then that case becomes primary
and the others become sensitivity checks.

---

## D5 — Umbra-only is carried as a baseline constraint, flagged for relaxation

**2026-07-28.** The optimiser assumes umbra-only science, matching published ConOps, but must report the
duty-cycle cost so relaxation can be argued if needed.

**Why:** the constraint exists for solar background and thermal stability in the *primary* science. Whether
the ALP analysis needs it is a separate question (Q5). Under dawn/dusk SSO it is close to fatal.

**Reversed if:** Q5 resolves that non-umbral observing is acceptable for this channel.

---

## D6 — DarkNESS-2 lobster-eye optics deferred

**2026-07-28.** Out of scope. Not modelled, not mentioned in projections.

**Why:** no design parameters exist yet. Speculating on optics would contaminate a study whose value is
that every number is traceable.

**Reversed if:** lobster-eye parameters (focal length, effective area vs energy, FOV) become available.
Then it is a clean extension: only the product $A\Omega$ matters for a diffuse signal, so the study can
evaluate it without restructuring — see [[01-physics/sensitivity-scaling]].

---

## D7 — Yamamoto's text coherence mass is not inherited

**2026-07-28.** Use $m_{\rm coh}$ computed from our own path integral. Their text value of
$3.3\times10^{-6}$ eV is inconsistent with both their own Figure 7 (knee at $1.26\times10^{-5}$ eV) and
their stated 6 $R_E$ integration path.

**Why:** established by digitising their figure; see [[01-physics/coherence-and-mass-reach]].

**Reversed if:** an erratum or the authors clarify.

---

## D8 - Spectral-background simulator deferred until the state-table interface is stable

**2026-07-30.** The next implementation is the Yamamoto geomagnetic validation and frame-state table in [[04-plan/next-step]]. A generalized spectral-background simulator is retained as a later work package.

**Why:** the field integral, orbit/attitude geometry, and nuisance-covariate interface can be validated without claiming a DarkNESS-specific particle count spectrum. Completing them first establishes the simulator inputs and tests whether the ALP regressor is identifiable at all.

**Reversed if:** a validated DarkNESS flight-like background data set or an immediately usable Fermilab Geant4 event model becomes available and requires an earlier integration test.

---

## D9 - The four-field Suzaku geometry validation is the accepted kernel gate

**2026-07-31.** The Yamamoto geometry cohort passes after combining the standard
3x3 and 5x5 cleaned XIS GTIs for each selected detector and merging overlaps.
All 23 primary observations match the thesis exposure table within 0.1 ks,
converge numerically, and populate the published field-integral bins.

**Why:** the earlier one-file ingestion could produce a false pass while losing
large fractions of exposure. The multi-file GTI union and thesis-exposure gate
now test the archived observation interval independently of the field result.

**Reversed if:** a later audit identifies a different authoritative observation
cohort, screening convention, or a frame/field-model error.

---

## D10 - ISS-like is the first DarkNESS baseline, not the final orbit trade

**2026-07-31.** The first DarkNESS mission-state vertical slice uses an
ISS-like orbit in 2027. The SSO cases remain later sensitivity cases and are not
required to prove the FORMS-to-ALP state-table interface.

**Why:** one concrete orbit is needed to advance the pipeline without turning
the first baseline into an orbit trade study. DarkNESS's manifested orbit is
still not treated as fixed.

**Reversed if:** the launch orbit is manifested before the baseline is
completed.

---

## D11 - Galactic Center pointing is the nominal baseline; optimization is separate

**2026-07-31.** The baseline holds an inertial Galactic Center boresight whenever
the target is accessible. It does not claim that ALP science requires Galactic
Center pointing. A fixed maximum slew rate of 1.5 deg/s is carried; detailed
power and thermal constraints are excluded. The first vertical slice is
on-axis, and the 20 deg FOV is added through a later sampling-convergence test.

**Why:** this represents nominal DarkNESS science operations and gives the
pointing optimizer a clear, unoptimized control case. Deferring FOV averaging
keeps an unresolved quadrature choice from blocking the mission-state
interface.

**Reversed if:** the nominal DarkNESS target strategy changes or payload access
constraints make inertial GC tracking infeasible.

---

## D12 - SmallSat 2027 is a DarkNESS case study, not a flight commitment

**2026-09-08.** The minimum publishable unit uses the published DarkNESS-class platform and ConOps as a
reference case. It compares the nominal parasitic schedule with one bounded alternative, but it does not
claim that the current flight mission has adopted an ALP campaign.

**Why:** the earlier framing mixed actual-flight analysis, a retasked/follow-on observatory, and a generic
SmallSat trade. The case-study boundary preserves the mission-analysis contribution without inventing
operational authority.

**Reversed if:** the DarkNESS team commits observing time and supplies the configuration-controlled orbit,
attitude constraints, and analysis inputs for a flight ALP search.

---

## D13 - Identifiability precedes the coupling curve

**2026-09-08.** The next result is the conversion kernel after projection against orbit/background
covariates for a nominal and bounded paired schedule. The primary sensitivity product is a limit on ALP
flux times $g_{a\gamma\gamma}^2$, or on the combined parent-decay normalization. A conventional
$g_{a\gamma\gamma}$ curve is a conditional translation.

**Why:** the particle background and conversion kernel share orbital drivers, and the incident relativistic
ALP flux is model dependent. A curve obtained before testing identifiability or declaring the source model
would be precise without being meaningful.

**Reversed if:** an independent background-control measurement makes the kernel effectively orthogonal to
the nuisance model and a specific parent-decay benchmark is adopted as the explicit result.

---

## D14 - No primary source channel until a common count-level screen

**2026-09-08.** Channel A (cosmological continuum) and Channel B (Galactic narrow feature) remain co-equal
until they are compared with the same detector response, background model, and operational constraints.

**Why:** Channel A has pointing freedom but weak spectral discrimination. Channel B is pointing-constrained
but better matched to skipper-CCD spectroscopy and the nominal Galactic Centre campaign. Geometry alone
does not decide the stronger measurement.

**Reversed if:** the common screen shows a robust winner across the reference and conservative background
cases.

---

## D15 - The Milky Way feature and extragalactic continuum are linked source components

**2026-09-08.** For the reference two-body decay $\chi\rightarrow aa$, the
Milky Way feature and extragalactic continuum are derived and fitted as
components of one source hypothesis with a shared decay normalization. This
decision revises the earlier treatment of Channel A and Channel B as
independent alternatives in D3 and D14. Their information contributions may
still be compared for mission design.

**Why:** both components arise from the same parent abundance, lifetime,
branching fraction, and daughter multiplicity. Choosing one before deriving
their relative normalization can discard signal or misstate the physical
hypothesis.

**Reversed if:** the project adopts a different source mechanism that produces
only one component, or a validated calculation proves one component
negligible in the declared analysis domain.

---

## D16 - Science definition precedes additional mission optimization

**2026-09-08.** The current work package is the source, detection-channel, and
scientific-viability gate in [[04-plan/next-step]]. The DarkNESS mission-state
and identifiability slice is preserved in
[[04-plan/mission-identifiability-work-package]] and begins after this gate.

**Why:** mission requirements depend on the source spectrum, measurable
parameter combination, and count scale. The provisional conditional coupling
reach is weaker than standard limits on the photon coupling. Mission
optimization is only worthwhile after the combined allowed parameter space
has been evaluated.

**Reversed if:** an independently reviewed source-to-count calculation and
allowed benchmark are supplied as controlled project inputs.

---

## D17 - Signal counts scale as the second power of the photon coupling

**2026-09-08.** With the parent decay rate treated as an independent source
parameter, the converted photon counts scale as
$g_{a\gamma\gamma}^{2}f_\chi\mathcal B_{aa}/\tau_\chi$. The earlier
$g_{a\gamma\gamma}^{4}$ statement in the sensitivity note was incorrect and
has been corrected.

**Why:** the incident ALP intensity is set by the parent decay. The weak-mixing
conversion probability supplies one factor of $g_{a\gamma\gamma}^{2}$.

**Reversed if:** a specific microscopic model is adopted in which the parent
decay width is itself tied to $g_{a\gamma\gamma}$. That model must derive and
declare the resulting dependence.

---

## D18 - The headline question is the ALP ConOps, not the coupling reach

**2026-09-17.** The research question is now: using the DarkNESS platform,
what observing ConOps maximises the identifiable geomagnetic conversion
signal against particle and diffuse backgrounds, and what does it require of
the mission. The ALP ConOps is free of the sterile-neutrino pointing but
keeps the platform constraints. Umbra-only versus sunlit imaging is carried
as two named cases (extends D5). The 2026-09-08 coupling-reach question
becomes the journal-extension follow-on.

**Why:** the provisional coupling reach sits inside stellar and helioscope
bounds, so it cannot be the headline. The identifiability of conversion
variation against geomagnetically correlated background is the open,
falsifiable result, and the student starts from the geometry and constraint
map that answers it.

**Reversed if:** the science-definition gate finds an allowed source benchmark
within DarkNESS reach, which would restore the coupling question as primary.

---

## D19 - The toolkit is small stdlib scripts written here, with packages kept minimal

**2026-09-17.** Student-path scripts in `src/darknessalp/` are stdlib, one
function per file, each with a known-answer test. `numpy`, `scipy`,
`astropy`, `matplotlib` are allowed where they genuinely simplify (analysis
layer, plots, test oracles); anything new goes into `requirements.txt`. No
FORMS in the student path — it is the mentor's later cross-check. The field
model is IGRF-14 with `lmax` as the fidelity knob (1 = tilted dipole for
scans); CHAOS is a later comparison. Latitude is geocentric; the ECI frame
is the mean equinox of date. J2 nodal regression stays in the orbit model.
Supersedes the 2026-07-28 `skyfield`/`ppigrf` recommendation in
[[02-mission-analysis/tooling]].

**Why:** teaching codebase. The trig and the integral are the learning
content and the known-answer checks are what make generated code safe. The
pure-Python IGRF is fast enough (20 ms per ray) that a library buys nothing.

**Reversed if:** the analysis layer outgrows what a few hundred lines can
carry, or a student cannot get through Stages 1–3 with the scripts as
scaffolding.

---

## D20 - Earth-facing boresight is allowed; thermal is deferred

**2026-09-17.** The PI confirmed the platform does not forbid pointing the
aperture at the Earth. Thermal margin is ignored for now. Radiator panels
and direct-Sun avoidance remain constraints to model. Consequence: the
Earth-occultation frames of a fixed target are a candidate $K$-off control
(≈2 % of sky $K$ at matched cutoff rigidity), which makes "keep science
frames running through occultation" a requirement candidate (Q21).

**Why:** the on/off pair is the most useful thing the study can hand the
mission, and occultation delivers one without slews or a new ADCS mode.

**Reversed if:** the thermal model or the radiator geometry (Q4) shows an
Earth-facing boresight is not sustainable for a useful fraction of an orbit.

---

## D21 - The library is numpy/scipy/astropy by topic; the run file is a notebook

**2026-09-17.** Supersedes the stdlib rule in D19. `src/darknessalp/` is
organised as topic subpackages (`frames`, `orbit`, `dynamics`,
`kinematics`, `pointing`, `field`, `geometry`, `background`, `sim`) of
functions on numpy arrays. astropy owns time and frames, scipy owns
integration and rotations. Custom code only where no package does the job.
Run scripts live outside `src/`: `scripts/` for thin CLI tools and
`jupyter/` notebooks that build the simulation sequence and show results.
Still four packages; still no FORMS in the student path.

**Why:** the student should not have to know how an integrator works, and
the scripting should be as short as possible even for advanced modelling.
Vectorising the line-of-sight integral over rays made it 60× faster and
half the length; astropy frames removed the equinox-of-date caveat. The
known-answer checks carried over, which is what made the rewrite safe.

**Reversed if:** the notebook-as-run-file stops being reproducible, or a
student cannot follow the array conventions — then a thin script layer
comes back.

---

## D22 - Testing is five layers, and pytest is the runner

**2026-09-17.** Known answers, invariants, cross-checks against
independent implementations, gates against published numbers, and pinned
end-to-end regressions. `python -m pytest` is the command; `unittest
discover` is banned because it silently collected zero tests from
pytest-style files. Regression pins are descriptions, not requirements:
when one moves, recompute it deliberately and say why.

**Why:** the project's credibility rests on numbers a reader can check
elsewhere, not on the code running. The published-number layer earned
this immediately by finding that `circular_orbit` measured altitude
above the IGRF reference sphere rather than the WGS84 equatorial radius.

**Reversed if:** the suite gets slow enough that people stop running it,
in which case the gates move to a separate slow marker.

---

## D23 - The repository keeps three notebooks

**2026-09-17.** `jupyter/` holds the simulation run file
(`darkness_alp_sim.ipynb`), the Yamamoto 2020 Figure 7 regeneration with
the axion-limit data, and the allowed-signal ceiling screen. The FORMS
sample notebooks and the old Suzaku/Yamamoto exploration notebooks are
deleted, along with the `yamamoto/` and `bfield/` packages and their
tests that nothing else used. FORMS remains available in `routines/`
for the PI's own later cross-check; `missions/` is removed too.

**Why:** the old notebooks encoded a superseded architecture and kept
dependencies (pyIGRF, chaosmagpy, the untracked Suzaku archive) alive
for no current result. Everything is recoverable from git history.

The two Suzaku validation records in `02-mission-analysis/` stay as the
provenance for D9, marked archived, pointing at the data-free gate that
replaced them.

**Reversed if:** the Suzaku cohort validation is needed again, in which
case it returns as a topic package with tests, not as notebooks.

---

## D24 - FORMS leaves the repository

**2026-09-19.** `routines/`, `src/routines/`, `AGENTS.md`, the FORMS
lines in `requirements.txt`, `04-plan/forms-integration.md` and the
`06-yamamoto-suzaku-archive/` stubs are deleted. `chaosmagpy` and
`data/bfield/CHAOS-8.3.mat` go with them; the CHAOS comparison stays a
listed next step. `freeflyer/` held only a README and is removed until
there is a script to put in it. The Yamamoto Fig. 7 PNG is generated
into `outputs/`, not tracked.

**Why:** one model, one path. FORMS was never in the student path (D21)
and the cross-check it promised is now the test suite (D22). Every file
in the tree should be something the student or mentor runs or reads.

**Reversed if:** an independent propagator cross-check is wanted; it
returns as a script under `scripts/` with its own requirement line.

---

## Links

- part of [[ALP]]
- unresolved: [[open-questions]]
