---
type: derivation-contract
tags: [darkness, alp, physics, derivation, validation]
created: 2026-09-08
updated: 2026-09-08
status: active
---

# Detection-channel derivation contract

This note defines what a complete and reviewable derivation must establish
before mission requirements or a projected sensitivity can be claimed. The
equations below define the intended structure. Numerical factors, units, and
conventions remain subject to line-by-line verification against primary
sources and analytic tests.

## Physical hypothesis

A nonrelativistic parent species $\chi$, with mass $m_\chi$, present-day dark
matter fraction $f_\chi$, lifetime $\tau_\chi$, and branching fraction
$\mathcal B_{aa}$, decays through

$$
\chi\rightarrow a+a.
$$

The daughters have energy $E_0\simeq m_\chi/2$ when $m_a\ll m_\chi$. They are
relativistic messenger particles. They are not the local cold dark matter.

The two-body source produces two linked observable components:

1. Milky Way decays produce a direction-dependent, Doppler-broadened feature
   near $E_0$.
2. Extragalactic decays produce an approximately isotropic continuum below
   $E_0$ through cosmological redshift.

These are components of one source hypothesis with a shared decay
normalization. Operational emphasis may differ, but a physical forecast must
derive both and state any reason for omitting either.

## Parameter of interest

In the weak-mixing limit, the incident flux is proportional to
$f_\chi\mathcal B_{aa}/\tau_\chi$ and the conversion probability is
proportional to $g_{a\gamma\gamma}^{2}$. The leading count normalization is
therefore

$$
\Theta = g_{a\gamma\gamma}^{2}
\frac{f_\chi\mathcal B_{aa}}{\tau_\chi}.
$$

The data do not determine $g_{a\gamma\gamma}$ alone. A coupling curve is a
conditional translation for declared $f_\chi$, $\mathcal B_{aa}$, and
$\tau_\chi$.

For $\tau_\chi$ comparable to the age of the universe, the lifetime also
changes the extragalactic spectral shape through the decay history. In that
regime, $\Theta$ is a normalization label and the response template must retain
explicit $\tau_\chi$ dependence. The derivation must also distinguish a
primordial parent fraction from a present-day surviving fraction.

## Derivation chain

### 1. Source intensity at Earth

The Milky Way differential intensity per solid angle should reduce to a form
equivalent to

$$
\frac{d\Phi_a^{\rm MW}}{dE\,d\Omega} =
\frac{f_\chi\mathcal B_{aa}}{4\pi m_\chi\tau_\chi}
\frac{dN_a}{dE}
D_\chi(\hat n),
\qquad
D_\chi(\hat n)=\int_{\rm los}\rho_\chi(s,\hat n)\,ds,
$$

with $dN_a/dE=2\delta(E-E_0)$ before velocity and detector broadening. The
derivation must state whether $\rho_\chi$ already includes $f_\chi$ and must
avoid applying the fraction twice.

The extragalactic differential intensity should be derived from the decay
emissivity in an expanding universe, including the relation
$E'=E(1+z)$, the expansion rate $H(z)$, the decay history, and the two-daughter
spectrum. The final expression must be checked against the energy-density
form in Dror, Murayama, and Rodd and against the Yamamoto normalization.

Required source checks:

- integrate each differential spectrum and recover the expected total number
  or energy density
- recover a narrow feature with fractional physical width of order the halo
  velocity dispersion before detector smearing
- recover a continuum with support only for $E\leq E_0$
- confirm the Milky Way and extragalactic relative normalization for the same
  $f_\chi$, $\tau_\chi$, and $\mathcal B_{aa}$
- reproduce one published benchmark spectrum without fitting a free scale.

### 2. ALP-photon propagation

Start from the interaction

$$
\mathcal L_{a\gamma\gamma} =
-\frac{1}{4}g_{a\gamma\gamma}aF_{\mu\nu}\widetilde F^{\mu\nu}.
$$

For a relativistic ALP travelling along $s$, derive the three-state mixing
equation for two photon polarizations and the ALP. In a fixed transverse
basis, the leading amplitudes have the structure

$$
\mathcal A_j(E)=
-i\frac{g_{a\gamma\gamma}}{2}
\int ds\,B_j(s)
\exp\left[i\int_0^s q(s')\,ds'\right],
$$

$$
q(s)=\frac{m_a^2-\omega_{\rm pl}^2(s)}{2E},
\qquad
P_{a\rightarrow\gamma}=|\mathcal A_1|^2+|\mathcal A_2|^2.
$$

The calculation must integrate signed transverse vector components. An
integral of the scalar magnitude $|\mathbf B_\perp|$ is not equivalent when
the projected field changes direction.

Required propagation checks:

- constant field and constant plasma reproduce the analytic sinc-squared
  result
- $m_a,\omega_{\rm pl}\rightarrow0$ reproduces the coherent vector integral
- a sign-changing field demonstrates cancellation at amplitude level
- basis rotation leaves $P_{a\rightarrow\gamma}$ unchanged
- numerical refinement converges for representative LEO rays
- ray direction, path orientation, integration boundary, and SI-to-natural
  unit conversions are explicit
- internal geomagnetic, external magnetospheric, plasma, and absorption
  assumptions are separated so their effects can be tested individually.

### 3. Photon intensity and detector counts

To leading order, the converted photon inherits the ALP energy and direction.
The incident photon intensity is

$$
I_\gamma(E,t,\hat n)=
I_a(E,\hat n)P_{a\rightarrow\gamma}(E,t,\hat n).
$$

For time interval $i$ and reconstructed energy bin $j$, the signal expectation
must take the form

$$
\mu^{\rm sig}_{ij}=\int_{\Delta t_i}dt
\int d\Omega\int dE\,
I_a P_{a\rightarrow\gamma}
A_{\rm proj}(\hat n,t)
T_{\rm ap}(E,\hat n)
{\rm QE}(E)
\epsilon(E,t)
R_j(E,t).
$$

The response derivation must distinguish geometric area, projected area,
active area, field-of-view acceptance, quantum efficiency, event-selection
efficiency, live time, and energy redistribution. The published 12 cm$^2$
geometric area is not automatically the effective collecting area.

Required detector checks:

- an isotropic constant-brightness source recovers the expected grasp
- a monochromatic input conserves counts through redistribution
- masking and live-time losses are applied once
- on-axis and field-of-view-averaged kernels converge to the same result as
  the aperture narrows
- radiation-age response cases are carried as distinct documented inputs.

### 4. Likelihood and identifiable claim

The full expectation is

$$
\mu_{ij}(\Theta,\boldsymbol\beta)=
\Theta k_{ij}+\sum_p Z_{ijp}\beta_p.
$$

The design matrix $Z$ must include the background and environment terms that
can covary with the conversion kernel. The forecast must report the
information remaining after nuisance projection. The raw range of the field
integral is insufficient.

The result hierarchy is:

1. a source-agnostic limit on converted brightness or on
   $g_{a\gamma\gamma}^{2}I_a$ for a declared spectrum
2. a limit on $\Theta$ for the joint parent-decay source model
3. a conditional $g_{a\gamma\gamma}$ curve for declared source parameters
4. a comparison with existing constraints in the same parameterization.

Confidence construction, nuisance priors, signal injection, bias, and
coverage must be stated. The likelihood should fit the linked Milky Way and
extragalactic components jointly before evaluating component-specific
operational simplifications.

## Scientific viability gate

Before mission optimization, determine whether any benchmark satisfying
current constraints on $g_{a\gamma\gamma}$ and invisible dark matter decay can
produce an observable DarkNESS count rate. Existing stellar and helioscope
limits on the photon coupling are substantially below the provisional
DarkNESS conditional coupling scale. The project must therefore test the
allowed combined parameter space, not compare coupling curves in isolation.

Possible dispositions are:

- **Continue:** at least one documented allowed benchmark is testable, or the
  mission improves an existing limit on $\Theta$.
- **Revise:** the measurement is not competitive in particle parameter space,
  but it yields a publishable requirement or validated search method for a
  future platform.
- **Redirect:** all allowed benchmarks are many orders below the reachable
  count rate and no distinctive mission-method result remains.

## Independent review packet

An Astra derivation review should receive a bounded packet containing:

1. this contract
2. the primary source equations and adopted notation
3. a symbolic derivation with every Jacobian and unit conversion shown
4. the analytic checks and their numerical results
5. the code functions that implement each equation
6. a list of unresolved physics choices.

The requested review should identify the first invalid step, missing factor,
or unsupported approximation. It should not be asked to invent an end-to-end
derivation without this declared target.

## Primary sources

- Yamamoto et al. 2020: https://arxiv.org/abs/1906.04429
- Dror, Murayama, and Rodd 2021, corrected version:
  https://arxiv.org/abs/2101.09287
- Marsh et al. 2022: https://arxiv.org/abs/2107.08040
- Nygaard, Tram, and Hannestad 2021:
  https://arxiv.org/abs/2011.01632
- Alpine et al. 2025: https://arxiv.org/abs/2505.16981
- Alpine et al. 2026: https://arxiv.org/abs/2602.02461

## Links

- source chain: [[alp-signal-chain]]
- current work: [[../04-plan/next-step]]
- sensitivity: [[../03-sensitivity/method]]
- decisions: [[../decisions]]
- open questions: [[../open-questions]]
