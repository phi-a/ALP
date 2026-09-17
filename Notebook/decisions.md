---
type: note
tags: [darkness, alp, decisions]
created: 2026-07-28
updated: 2026-09-08
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

## Links

- part of [[ALP]]
- unresolved: [[open-questions]]
