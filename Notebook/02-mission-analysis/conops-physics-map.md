---
type: note
tags: [darkness, alp, conops, mission-analysis, physics]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# ConOps ↔ physics map

What the ConOps variables actually touch in the ALP physics DarkNESS can
probe, and the three consequences that set the design. From the
2026-09-17 thinking session; tools in [[tooling]], numbers in
[[geomagnetic-integral]] and [[pointing-optimization]].

## What DarkNESS can probe, by channel

| Channel | Source spectrum | Pointing enters via | Verdict |
|---|---|---|---|
| χ→aa Milky Way line | line at $m_\chi/2$, width from halo velocity | $S_\phi(l,b)$ **and** $K$ | joint; skipper resolution is the discriminant |
| χ→aa extragalactic continuum | redshifted continuum | $K$ only (isotropic) | **pointing-free** channel |
| primordial cosmic ALP background (moduli decay, Conlon & Marsh 2013) | fixed thermal-ish shape, mean ~0.1–1 keV, tail into band | $K$ only (isotropic) | same machinery, different template; $\Delta N_{\rm eff}$-bounded |
| solar axions, GECOSAX (Davoudiasl & Huber 2006; Fraser+ 2014) | Primakoff, peaks 3 keV | point at the **occulted Sun** from umbra | $\propto g^4$, needs ~10⁴ cm²; not competitive at 12 cm² |
| ultralight axion / dark photon (PTEP 2026, ELF magnetometers) | 10⁻¹⁵ eV, Hz | — | different regime, ignore |

Everything DarkNESS can do sits in rows 1–3, and rows 2–3 share one
kernel $K(\mathbf r_{\rm sc},\hat n,E)=|\int_0^{L}B_\perp e^{iqs}ds|^2$
with no sky dependence. That is why the ConOps question is a geometry
question first.

## Who depends on what

The identifiability problem in one table. Position is $\mathbf r_{\rm sc}(t)$,
pointing is $\hat n$, sky is $(l,b)$ of $\hat n$.

| Term | position | pointing | sky | time |
|---|---|---|---|---|
| $K$ (extragalactic) | yes | yes | no | via position |
| $K \cdot S_\phi$ (Galactic line) | yes | yes | yes | via position |
| NXB (particle) | yes — $R_c \propto \cos^4\lambda_m/r^2$, SAA | **no** | no | solar cycle, storms |
| CXB | no | no | no (20° cone averages cosmic variance) | no |
| GRXE + bright sources | no | no | yes | no |
| Earth limb / atmosphere | yes | yes (limb angle) | no | day/night |
| Sun | yes | yes (Sun angle) | no | eclipse |

Read across the $K$ row against the NXB row: **at fixed position, pointing
moves $K$ and not NXB.** That is the single lever the ConOps has. The
limb term is the only background that couples position and pointing the
same way $K$ does, so limb angle is the covariate to control hardest.

## Three consequences

**a. Pointing comes in tiers of mission cost.** The ALP objective
inherits the bus, payload and constraint set — not the other objectives'
pointing. What it inherits for free is the qualified ADCS mode, "Inertial
Science Pointing". Anything beyond that is a requirement handed back
(Q6: slew, settle, momentum, all `DN-TBC`).

| Tier | Pointing | New requirement | Role |
|---|---|---|---|
| 1 | one fixed inertial target | none | the floor |
| 2 | a fixed target per orbit, re-selected during occultation or a ground pass | one slew per orbit | the on/off pair from [[pointing-optimization]] |
| 3 | continuous field-tracking scan law | new ADCS mode, Q6 | upper bound on leverage |

Tiers 1–2 are computable with the toolkit in [[tooling]]: for each fixed sky direction, $K(t)$
modulates at the orbital period as the local $\mathbf B$ rotates past
the fixed $\hat n$, and so does $R_c(t)$. A sky map of
$\rho[K(t),R_c(t)]$ per target is the tier-1 figure and it is cheap; the
tier-2 answer is the best pair of targets from that map. Tier 3 is the
same cube $K[t,\hat n]$ read column-wise instead of row-wise, so nothing
in the toolkit changes — only the optimiser.

**b. Earth occultation gives the "off" state for free.** A fixed target
is behind the Earth for part of each orbit. Those frames look at the
night Earth, exactly the night-Earth NXB template every X-ray mission
uses. With a centred dipole at 420 km, magnetic equator:

| pointing | $B_\perp L$ | $K$ relative |
|---|---:|---:|
| zenith (sky) | 83 T m | 1 |
| nadir (through Earth, 420 km path) | 11 T m | 0.019 |

So occultation frames carry ~2 % of the sky $K$ at the same
$R_c$ — the on/off pair from the notes, delivered by orbital mechanics
instead of slews. This becomes a **mission requirement candidate**: keep
science frames running through occultation, and confirm the radiator
secondary-axis constraint permits an Earth-facing boresight. The PI
confirmed 2026-09-17 that Earth-facing is not forbidden (D20); the
frames-through-occultation requirement is Q21.

**c. Plasma is negligible for the keV path.** Worst case
$n_e\sim10^6$ cm⁻³ gives $\omega_{\rm pl}=3.7\times10^{-8}$ eV; the
coherence knee at 3 keV over the $r^{-3}$ scale length ($\sim r_0/2$) is
$m_a\approx2\times10^{-5}$ eV, so
$\omega_{\rm pl}^2/m_a^2\sim4\times10^{-6}$. Q17 closes at first order:
IGRF-only, no ionosphere, no plasmasphere. `DERIV`; recorded as A4 in
[[../open-questions]].

## Links

- part of [[../ALP]]
- constraints in: [[../00-baseline/darkness-conops]]
- kernel: [[geomagnetic-integral]]; objective: [[pointing-optimization]]
- tools: [[tooling]]
- feeds: [[../04-plan/mission-identifiability-work-package]]
- decisions: [[../decisions]] D18–D20; questions: [[../open-questions]] A4, Q21, Q22
