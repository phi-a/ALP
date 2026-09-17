---
type: note
tags: [darkness, alp, physics]
created: 2026-07-28
updated: 2026-09-08
status: active
---

# The ALP signal chain for DarkNESS

End-to-end: ALP flux arriving at the magnetosphere → conversion in the geomagnetic field along the line
of sight → photons in the DarkNESS band → counts. Everything traces to Yamamoto et al. 2020
(JCAP 02 (2020) 011), whose equation numbers are used throughout.

## Conversion probability

For a uniform perpendicular field over path length $L$ (Yamamoto eq. 2.10):

$$
P_{a \to \gamma} = \left( \frac{g_{a\gamma\gamma} B_\perp L}{2} \right)^{2} R(qL)
$$

$$
R(x) = \frac{2\,[1 - \cos x]}{x^{2}}, \qquad q = \frac{m_a^{2}}{2 E_a}
$$

$R \to 1$ in the coherent limit and falls as the phase $qL$ accumulates. The mass reach follows entirely
from that factor. See [[coherence-and-mass-reach]]. The realistic case is not a uniform field, so the
quantity DarkNESS actually needs is the phase-carrying line integral defined in
[[../02-mission-analysis/geomagnetic-integral]].

**The number that sets everything:** at $B_\perp L = 100$ T m, $P \approx 2.6\times10^{-17}$ for
$g = 10^{-10}$ GeV⁻¹. This is a search for a signal riding on top of the diffuse X-ray background, not a
signal that can ever be seen on its own. Consequences run through the whole design.

## Two linked source components

### Extragalactic continuum

Cosmological dark-matter decays produce relativistic ALPs. Redshifting over
the decay history turns the two-body feature into a continuum. The flux is
approximately isotropic.

Sky direction does not change the source term to zeroth order. Pointing can
therefore emphasize geomagnetic geometry. The smooth spectrum may be strongly
degenerate with diffuse X-ray backgrounds.

### Milky Way narrow feature

Galactic DM decays to two ALPs, each at $E_a = m_\phi/2$, giving a **line** whose intensity scales with
the DM column density along the line of sight:

$$
I_{a,\rm line} = \frac{S_\phi \Gamma_{\phi \to 2a}}{2\pi m_\phi}, \qquad S_\phi = \int_{\rm l.o.s.} \rho_\phi\, dr
$$

Here pointing enters through both $S_\phi(l,b)$ and the conversion kernel, so
the optimization is joint. $S_\phi$ peaks toward the Galactic Centre, which
the baseline ConOps already visits. The narrow feature also uses the
skipper-CCD energy response as a discriminator against smooth backgrounds.

Yamamoto's cyan region is the universal continuous component. The yellow
region is the Galactic monochromatic component.

### Joint-source requirement

For the reference process $\chi\rightarrow aa$, these components share the
same parent abundance, lifetime, branching fraction, and daughter
multiplicity. They are not independent physical hypotheses. The source
derivation and reference likelihood must include both. A component-specific
analysis is acceptable only after the joint model establishes that the omitted
component is negligible or uninformative for the stated case.

The continuum permits broad sky access but has weak spectral discrimination.
The Milky Way component has a narrower spectral template and overlaps the
nominal Galactic Centre program. Mission analysis may compare their
information contributions while preserving the shared normalization.

## Counts model

The chain is the same one already implemented for the sterile-neutrino study in `LimitCalculation`, with
one new factor inserted:

$$
S_{ij} = \int_{\Delta t_i}\! dt \int\! dE \int\! d\Omega \;
I_a(E, \hat n, t)\; P_{a\to\gamma}(E, \hat n, t)\; A_{\rm eff}(E)\; R_j(E)\; \epsilon(E,t)
$$

- $I_a$ contains the linked Milky Way and extragalactic components.
- $P_{a\to\gamma}$ requires orbit, attitude, magnetic-field, plasma, and path models.
- $A_{\rm eff}$, $R_j$, $\epsilon$ include 12 cm² geometric area, QE(E), masking and live fractions, Gaussian smearing
  at σ_E, and cut efficiency. See [[../00-baseline/darkness-parameters]].

Note $P_{a\to\gamma}$ carries **no area dependence**. Conversion happens in the magnetosphere. The
detector simply sees an added diffuse surface brightness. Grasp is the
appropriate figure of merit for a diffuse source.

## The within-FOV gradient

Yamamoto could treat $B_\perp L$ as constant across an 18′ Suzaku field. Across DarkNESS's 20° cone it is
not constant. $B_\perp$ varies appreciably from one edge of the aperture to the other. Two
consequences:

1. The signal model must integrate $P$ over the FOV solid angle, not evaluate it on the boresight.
2. That gradient is a **discriminant**. A real conversion signal has a specific brightness gradient across
   the field set by the field geometry; CXB and instrumental background do not. Whether the statistics
   support using it is an open question, but it is a discriminator Suzaku never had.

## What must be declared

The Yamamoto translations carry an assumed dark-matter lifetime, density, and
source normalization. That study also neglects attenuation and anisotropy
caused by conversion in interstellar and intergalactic fields. A DarkNESS
projection must either adopt those assumptions explicitly or replace them
with a new derived source model.

The incident keV ALPs in this chain are relativistic daughters of a heavier dark-matter parent. They are
not the local cold ALP dark matter population. The model-independent measurement is a limit on the
incident ALP flux times $g_{a\gamma\gamma}^2$; a limit on $g_{a\gamma\gamma}$ alone is a conditional
translation.

## Links

- part of [[../ALP]]
- mass reach: [[coherence-and-mass-reach]]
- what it buys: [[sensitivity-scaling]]
- field integral: [[../02-mission-analysis/geomagnetic-integral]]
- derivation contract: [[detection-channel-derivation-contract]]
- prior broad survey: [[../darkness_alp]]
