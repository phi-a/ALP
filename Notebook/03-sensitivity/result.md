---
type: result
tags: [darkness, alp, result, paper, sensitivity, identifiability]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# The channel result

This note states what a DarkNESS-class skipper-CCD NanoSat can and
cannot claim about axion-like particles from dark-matter decay
converting in the geomagnetic field, from the chain derived in
[[../01-physics/block-a-conversion]] to [[../01-physics/block-d-claim]],
and which parts of that are the paper's contribution. It is the prose
the paper is written from and the target the parallel derivation is
compared against. Keys refer to [[../references]].

## Claim

A dark-matter parent $\chi$ decaying to two relativistic ALPs gives a
narrow line at $m_\chi/2$ from the Milky Way halo and a redshifted
continuum below it from the universe; an ALP crossing the geomagnetic
field converts to an X-ray photon with probability
$(g/2)^2\lvert\int\mathbf B_\perp e^{iqs}ds\rvert^2$, so the converted
brightness is proportional to $\Theta = g^2 f/\tau$ times a kernel
$K$ that the orbit and pointing set. On the reference DarkNESS
schedule over 187 days, the 90 % statistical limit on $\Theta$ lies
$4\times10^5$ to $2\times10^6$ above the ceiling allowed by the
stellar bound on $g$ and the Planck 2018 bound on decaying dark
matter; no allowed model is detectable, and the gap does not close
with exposure. The analysis establishes instead how such a search
must be built: the signal is identified by its energy spectrum, not
its time dependence; the halo line carries the sensitivity; and the
geomagnetic confounders that track $K$ in time cost 5 % of the
information once the spectrum is fitted and 94 % without it.

## 1. The hypothesis and what is measured

$\chi$ has mass $m_\chi$ in the keV range, present-day share $f$ of
the dark matter (with the branching ratio to $aa$ folded in), and
lifetime $\tau \gg t_U$. The daughters are relativistic messengers,
not the local dark matter. The data constrain the product $\Theta$;
a value of $g$ alone follows only for a declared $f/\tau$, and the
converted brightness per unit kernel is the source-agnostic quantity
beneath both.

## 2. The chain

Each block starts from the origin equation, not from `[Yam20]`, and
ends in checks that are tests in the repository.

**Conversion.** From the $g\,a\,\mathbf E\cdot\mathbf B$ interaction
`[RS88]` to the first-order amplitude, integrating the transverse
field as a vector so that a rotating field partly cancels. Uniform
field gives $2(1-\cos qL)/(qL)^2$; $g = 10^{-10}$ GeV⁻¹ and
$B_\perp L = 100$ T m give $P = 2.45\times10^{-17}$ (`[Yam20]` eq
2.13). Plasma, QED and Faraday terms are each below $10^{-4}$ of the
phase for DarkNESS. A ray ends at 10 $R_E$ or at the Earth; the
transparent boundary near 150 km, not the surface, is the correct
inner end for occulted rays (Q23).

**Source.** One count of decays gives both components with one $f$
and one $\tau$. The full-sky halo column from the NFW model matches
`[DMR21]` to 1 %; the Milky Way and extragalactic energy densities
stand in ratio 2.3 and exceed the CMB below $10^4\,t_U$, as `[DMR21]`
state; the continuum reduces to `[Yam20]`'s $E^{1/2}$ law with the
sign of $\Omega_\Lambda/x^3$ corrected. Today's share is the right
convention because it is what the halo measures.

**Counts.** Area 12 cm², a 20° cone (0.0955 sr), a 50 nm Al window,
500 µm of silicon, a 50 % live fraction and a 169 eV resolution enter
as separate factors, each applied once; a uniform sky recovers
$I\,A\Omega\,\Delta E\,\Delta t$ exactly and redistribution conserves
counts. On the reference day the chain reproduces the earlier ceiling
(D28) within its conventions.

**Likelihood.** Counts are Poisson in a model linear in $\Theta$ and
the background amplitudes; the Fisher matrix profiled over CXB, a
cutoff-rigidity particle proxy, an Earth-limb term and the Galactic
ridge gives the error on $\Theta$ and the share of information that
survives. Injected signals are recovered without bias and with the
stated coverage.

## 3. The gate

$\Theta_{\max} = (0.47\times10^{-10}\ {\rm GeV^{-1}})^2\times
4.0\times10^{-3}\ {\rm Gyr^{-1}} = 8.8\times10^{-24}$ GeV⁻² Gyr⁻¹
(`[DHV22]`, `[NTH21]`). At $\Theta_{\max}$ the reference day yields
$2.4\times10^{-5}$ signal counts on $4.5\times10^{5}$ to
$6.4\times10^{6}$ background counts; 187 days give
$4.5\times10^{-3}$. The 90 % limit is $3.8\times10^{-18}$ (CXB and
particle background) to $1.6\times10^{-17}$ GeV⁻² Gyr⁻¹ (with the
placeholder ridge model), $4\times10^{5}$ to $2\times10^{6}$ above
$\Theta_{\max}$; in $g$ at the allowed $f/\tau$, $3$–$6\times10^{-8}$
against $0.47\times10^{-10}$ GeV⁻¹. A limit set by counting improves
as the square root of exposure and grasp, so the gap corresponds to
$10^{11}$ in either. The disposition is Revise (D31): the study
continues as a method result.

## 4. What the analysis establishes

1. **Identifiability is spectral.** Across the science samples the
   kernel correlates with the limb term at 0.84 and with the particle
   proxy at −0.67. A fit to the time series alone keeps 6 % of the
   information on $\Theta$ ($\sigma$ ×15); a fit to the time-energy
   table keeps 95 %. The energy spectrum, not the orbital modulation,
   separates the signal from what moves with it. This is the design
   rule for any Earth-field search: resolution and a spectral template
   are worth more than kernel contrast.
2. **The line carries the search.** The joint and line-only limits
   coincide; the continuum alone is 37 times weaker. Sensitivity
   comes from a narrow feature at a known energy inside a wide field,
   which favours a detector with the resolution to see it and a
   pointing that maximises $\langle DK\rangle$, the halo column
   weighted by the kernel.
3. **The confounders cost little once modelled.** With the spectrum
   in the fit the four nuisance templates remove 5 % of the
   information. The central systematic of the method (Q7) is
   therefore the shape of the particle-background template, not its
   correlation with $K$.
4. **Against `[Yam20]`.** The same machinery in Suzaku-like geometry
   (570 km, 31°, 12 Ms, grasp 0.026 cm² sr, $K$ median
   $1.4\times10^4$ T² m²) gives a 90 % statistical floor of
   $5.2\times10^{-8}$ GeV⁻¹ at $\tau = t_U$; in their 3σ convention
   and grasp, $9\times10^{-8}$. Their eq 4.1 at 7 keV is
   $2.1\times10^{-7}$, 2.3 times above the floor, which meets the
   method note's gate 2 (within a factor of about 2). In converted
   brightness per unit kernel their Table 3 value is 85 times above
   the floor; how that table is normalised per T² m² is not
   resolved here and is carried as a caveat, not a claim.

## 5. Claim boundary

The measurement constrains the incident ALP intensity times $g^2$
for a declared spectrum. It does not constrain cold ALP dark matter,
does not treat a diffuse excess as conversion, and does not produce
a coupling curve except conditionally on $f/\tau$, the halo model and
the cosmology. The projected limit is statistical on idealised
templates and is a floor, not a forecast: the realistic limit is set
by template error, as `[Yam20]`'s was.

## 6. What would change it

The placeholder ridge model and the assumed particle level move the
limit by 4× and no conclusion. The occulted-ray endpoint (Q23) changes
the kernel-off control frames by 2.7×. The live fraction and
selection efficiency, constants here, become time-dependent nuisance
terms in a real fit. None of these reaches the $10^{5}$ in $\Theta$
the gate would need; only a source outside the $\chi\to aa$
hypothesis or a revision of the coupling or decay bounds does.

## Close

A DarkNESS-class NanoSat cannot reach any allowed
$\chi\to aa$ ALP model through geomagnetic conversion, by five to six
orders in $\Theta$, and no observing choice changes that. What it
can contribute is the anatomy of the measurement: spectral
identification, the halo line as carrier, and confounders that cost
5 % when the spectrum is used. Those three statements, each with a
number and a test behind it, are the paper.

## Links

- decision: [[../decisions]] D31
- method and gates: [[method]]
- scope and claim boundary: [[../04-plan/journal-contribution-scope]]
- blocks: [[../01-physics/block-a-conversion]], [[../01-physics/block-b-source]], [[../01-physics/block-c-counts]], [[../01-physics/block-d-claim]]
