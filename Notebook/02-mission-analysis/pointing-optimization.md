---
type: note
tags: [darkness, alp, mission-analysis, pointing, research-element]
created: 2026-07-28
updated: 2026-09-17
status: active
---

# Pointing optimization

Yamamoto analyzed the field geometries present in archival observations.
DarkNESS can compare executable pointing choices. The value of that choice
must be calculated after the science-definition gate and background nuisance
projection.

## The decision problem

Choose a boresight schedule $\hat n(t)$ over the science phase, subject to the
constraint set in [[../00-baseline/darkness-conops]], to maximize information
on the combined source amplitude $\Theta$.

The extragalactic source component is isotropic to leading order, so its sky
direction enters mainly through geomagnetic conversion and observing
constraints. The Milky Way component also carries the dark-matter column
density $S_\phi(l,b)$. The reference objective includes both with a shared
decay normalization. Component-specific objectives remain diagnostic cases.

## The objective is leverage, not magnitude

The tempting objective is "maximise $\langle (B_\perp L)^2 \rangle$." That is wrong, and getting it right
is most of the intellectual content here.

The measurement is a regression. Counts in frame $i$ are modelled as

$$
\mu_i = a\,x_i + b_i, \qquad x_i \equiv (B_\perp L)^2_i
$$

with $a \propto g_{a\gamma\gamma}^2 f_\chi\mathcal B_{aa}/\tau_\chi$
and $b_i$ the background. The ALP shows
up as a *correlation* of residual brightness with $x$. The variance of the fitted amplitude is

$$
\mathrm{Var}(\hat a)^{-1} \;=\; \sum_i \frac{x_i^2}{\mu_i} \;-\;
\frac{\left(\sum_i x_i/\mu_i\right)^2}{\sum_i 1/\mu_i}
$$

which in the background-dominated limit is the **weighted spread** of $x$, not its mean. Observations all
piled up at maximum $(B_\perp L)^2$ are nearly useless: with no variation in $x$, the ALP amplitude is
degenerate with the background normalisation.

So the schedule wants:

- a wide **range** of $(B_\perp L)^2$, including deliberately low-field pointings as the "off" state,
- balanced time between the extremes (leverage is maximised near a two-point design),
- everything else about those pointings as similar as possible, so that $x$ is the only thing varying.

That last requirement is the hard one and the real subtlety: if high-$x$ pointings systematically differ
in Earth-limb angle, geomagnetic latitude, or particle background, then **background correlates with $x$**
and the measurement is confounded. Confounding is expected to limit this
result. Yamamoto's limit was also systematics-limited. The optimizer must
penalize correlation between $x$ and every known background driver while it
maximizes spread.

That gives the actual objective: maximise Fisher information on $a$ **subject to** a decorrelation
constraint between $x_i$ and the background covariates. It is a design-of-experiments problem, which is a
much more defensible framing than "maximise the field."

## Where the field is: measured, not guessed

The local rule "maximise $B_\perp$ by looking across the field, minimise
it by looking along" is only half right for a *straight* line of sight
through a *curved* field. Dipole scan at 420 km, 2026-09-17
(`los_field_integral`, `lmax=1`, 13×12 directions, non-occulted):

| $\lambda_m$ | min $\|\mathcal A\|$ (where) | max $\|\mathcal A\|$ (where) | range in $K$ |
|---:|---|---|---:|
| 0° | 83 T m (zenith) | 253 T m (limb-grazing, toward magnetic N) | ×9 |
| 30° | 48 T m (el 40°, looking S) | 338 T m (limb-grazing N) | ×50 |
| 60° | **5 T m** (el 60°, looking S, along the field line) | 333 T m (limb-grazing N) | ×4000 |

Three things to carry:

1. **"Along the field" is a low-$K$ pointing only at high magnetic
   latitude**, where field lines are straight enough for a straight LOS
   to stay parallel. From the equator the along-axis ray gives 166 T m,
   twice zenith, because the LOS leaves the curved field line. At the
   equator zenith is the *minimum*.
2. **The maximum is always limb-grazing**: the longest path through the
   strongest field. So high $K$ ⇔ small limb angle by construction, and
   the limb/atmospheric background is correlated with the signal before
   any schedule is chosen. Model that covariate first, ahead of $R_c$
   (Q22).
3. **The accessible range of $K$ grows steeply with magnetic latitude.**
   ISS-like reaches $\lambda_m\approx60°$ on some passes; SSO every orbit.
   Re-read [[orbit-cases]] with this table.

The cleanest "off" state is not a sky pointing at all: the
Earth-occultation frame carries ≈2 % of the sky $K$ at the same
$R_c$ (11 vs 83 T m, [[conops-physics-map]]). An on/off pair that
differs in $(B_\perp L)^2$ and in as little else as possible is still the
single most useful thing this study can hand the mission; occultation
gives one for free, a second fixed target gives a sky-only one.

## Candidate strategies to evaluate

Tiered by mission cost in [[conops-physics-map]]: one fixed target, a
fixed target per orbit, a scan law.

| Strategy | Idea | Expect |
|---|---|---|
| Fixed inertial anti-Sun | Baseline, minimal ops | Low leverage because $x$ varies only with orbital phase |
| **Fixed target + occultation frames** | Use the night-Earth frames as the off state | Matched $R_c$, ×50 contrast, no slews; needs Q21 |
| Two fixed targets, alternated | Re-select during occultation or a ground pass | Sky-only on/off pair, one slew per orbit |
| Magnetic-perpendicular tracking | Continuously maximise $B_\perp$ | Max mean $x$, poor spread, limb-correlated |
| Stepped great-circle scan | Sample many geometries | Good spread, weak control of confounders |
| Opportunistic (GC/Cygnus as-is) | Parasitic on the baseline campaign | Uses the nominal allocation and establishes the floor |

The opportunistic case is important as a control: it quantifies what the ALP analysis is worth with **no**
dedicated pointing at all, which is the fallback if the mission cannot accommodate a modified schedule.

## Deliverable

1. $(B_\perp L)^2$ accessibility cube per orbit case (from [[geomagnetic-integral]])
2. Leverage-optimal schedule per orbit case, with the decorrelation constraint applied
3. The on/off pointing pair definition, in a form operations could actually fly
4. Projected constraint on $\Theta$ for each, followed by any conditional
   coupling translation

## Links

- part of [[../ALP]]
- why it matters: [[../01-physics/sensitivity-scaling]]
- inputs: [[geomagnetic-integral]], [[orbit-cases]]
- statistics: [[../03-sensitivity/method]]
- prerequisite: [[../04-plan/next-step]]
