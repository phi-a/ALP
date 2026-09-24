---
type: derivation
tags: [darkness, alp, physics, derivation, likelihood, identifiability, block-d]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Block D — the likelihood and the identifiable claim

This note states the likelihood for the DarkNESS ALP search, derives
the information on the signal amplitude that survives profiling the
backgrounds, fixes the hierarchy of claims, and answers the viability
gate with the chain of Blocks A–C on the reference day. Keys refer to
[[../references]].

## Result

Counts in time sample $i$ and energy bin $j$ are Poisson with mean

$$
\mu_{ij}(\Theta,\boldsymbol\beta) = \Theta\,k_{ij} + \sum_p \beta_p\,z_{pij},
\qquad
\Theta = g^2\,\frac{f}{\tau},
$$

$k_{ij}$ the joint line-plus-continuum template per unit $\Theta$ from
[[block-a-conversion]], [[block-b-source]] and [[block-c-counts]]
(one $f$, one $\tau$, $\tau \gg t_U$), and $z_p$ the background
templates. With Fisher information
$I_{ab} = \sum_{ij} t_{a,ij}\,t_{b,ij}/\mu_{ij}$ over all amplitudes,
the error on $\Theta$ after profiling is $\sigma_\Theta^2 =
[I^{-1}]_{\Theta\Theta}$, the surviving share of information is
$1/(I_{\Theta\Theta}[I^{-1}]_{\Theta\Theta})$, and the 90 % one-sided
limit is $\Theta_{\rm UL} = 1.28\,\sigma_\Theta$.

Reference day, 187 days, statistical only:

| | CXB + NXB | + placeholder GRXE |
|---|---|---|
| information kept, spectral fit | 0.945 | 0.937 |
| information kept, photometric fit | 0.061 | 0.074 |
| $\Theta_{\rm UL}$ [GeV⁻² Gyr⁻¹] | $3.8\times10^{-18}$ | $1.6\times10^{-17}$ |
| $\Theta_{\rm UL}/\Theta_{\max}$ | $4\times10^{5}$ | $2\times10^{6}$ |
| $g_{\rm UL}$ at $f/\tau = 4\times10^{-3}$ Gyr⁻¹ | $3.1\times10^{-8}$ | $6.3\times10^{-8}$ GeV⁻¹ |

Code: `likelihood.fisher`, `likelihood.profiled_sigma`,
`likelihood.information_fraction`, `likelihood.upper_limit`,
`likelihood.fit_amplitudes`.

## 1. The model

The signal enters linearly in $\Theta$ because $P \propto g^2$ (Block
A) and both source components are $\propto f/\tau$ (Block B); for
$\tau \sim t_U$ the template keeps its $\tau$ dependence and $\Theta$
is a label. The backgrounds and their templates on the reference day:

| $z_p$ | Time shape | Energy shape | Level | Tag |
|---|---|---|---|---|
| CXB | constant | $E^{-1.41}$ `[DLM04]` | 9.9 counts s⁻¹ | `EXT` |
| NXB | $R_c^{-1}$ (`background.nxb_proxy`) | flat | mean equal to CXB | `ASSUME` |
| Earth limb | $e^{-\theta_{\rm limb}/10^\circ}$ | flat | shape only, level unknown (Q22) | `ASSUME` |
| GRXE | constant (boresight fixed on the Centre) | $E^{-2}$ | `background.grxe_brightness`, cone-averaged; $27\times$ CXB | `ASSUME`, flagged "replace before quoting" |

$f_{\rm live}$ and $\epsilon_{\rm sel}$ vary with the particle rate and
belong in $Z$ as multiplicative nuisance terms; here they are the
constants of Block C. The likelihood is evaluated at the null,
$\mu = \sum_p \beta_p z_p$, in the Asimov sense.

## 2. Information after profiling

For Poisson cells, $I_{ab} = \sum_{ij}\partial_a\mu_{ij}\,
\partial_b\mu_{ij}/\mu_{ij}$, and for a linear model
$\partial_a\mu = t_a$. Inverting the full matrix profiles every
nuisance amplitude at once; the diagonal element is the variance of
$\hat\Theta$ with the others free. The fraction
$1/(I_{\Theta\Theta}[I^{-1}]_{\Theta\Theta})$ is 1 when no template
shares structure with $k$ and 0 when one reproduces it. With $10^4$
counts per cell the Gaussian limit is exact for our purpose.

Bias and coverage: an injected signal on a kernel-like template with a
constant and a confounder is recovered with bias below $0.15\,\sigma$
and 1-$\sigma$ coverage between 62 % and 74 % over 400 Poisson
realisations (`test_recovers_injected_amplitude_with_coverage`).

## 3. Reference day

Reference schedule (420 km, 51.6°, Centre in umbra, 39 samples,
6.5 h), $m_\chi = 7$ keV, 36 bins over 1–10 keV. Correlations across
the science samples: ${\rm corr}(K, R_c^{-1}) = -0.67$,
${\rm corr}(K, e^{-\theta_{\rm limb}/10^\circ}) = 0.84$,
${\rm corr}(K, \langle DK\rangle) = 1.000$.

| Template | Spectral fit: kept | $\Theta_{\rm UL}$ | Photometric fit: kept | $\sigma$ penalty |
|---|---|---|---|---|
| joint | 0.945 | $3.8\times10^{-18}$ | 0.061 | ×15 |
| line only | 0.954 | $3.9\times10^{-18}$ | 0.061 | ×16 |
| continuum only | 0.559 | $1.4\times10^{-16}$ | 0.061 | ×4.4 |

(CXB + NXB background; the placeholder GRXE raises every
$\Theta_{\rm UL}$ by 4× and changes no fraction by more than 0.1.)

Three things follow. The identifiability is **spectral**: a
time-only analysis keeps 6 % of the information because the limb and
cutoff templates track $K$; the energy dimension separates them. The
**line carries the search**: the joint and line-only limits coincide,
and the continuum alone is 37× weaker. And the confounders, though
strongly correlated with $K$ in time, cost only 5 % once the spectrum
is used, so the central systematic (Q7) is a template-shape problem,
not a correlation problem.

## 4. The hierarchy of claims

1. **Converted brightness per unit kernel**, continuum template,
   2–6 keV: $2.0\times10^{-7}$ (CXB + NXB) to $8.7\times10^{-7}$ (with
   GRXE) photons cm⁻² s⁻¹ sr⁻¹ per T² m². `[Yam20]` measured
   $2.4\times10^{-5}$, systematics-limited, on 12 Ms of Suzaku with
   8× less exposure-grasp. The 30–120× is a statistical projection on
   idealised templates and states the ceiling on what a real fit can
   do.
2. **$\Theta$**, the joint model: the table above.
3. **Conditional $g$** at the CMB-allowed $f/\tau = 4.0\times10^{-3}$
   Gyr⁻¹: $3$–$6\times10^{-8}$ GeV⁻¹, against `[Yam20]`'s
   $8.4\times10^{-8}$ at their parameters.
4. **Against constraints**: $\Theta_{\max} = (0.47\times10^{-10})^2
   \times 4.0\times10^{-3} = 8.8\times10^{-24}$ GeV⁻² Gyr⁻¹
   (`[DHV22]`, `[NTH21]`); $g_{\rm UL}/g_{\max} = 660$–$1340$.

## 5. The viability gate

At $\Theta_{\max}$ the reference day yields $2.4\times10^{-5}$ signal
counts (line $2.2\times10^{-5}$) on $4.5\times10^{5}$ to
$6.4\times10^{6}$ background counts; 187 days give $4.5\times10^{-3}$.
The 90 % limit sits $4\times10^{5}$ to $2\times10^{6}$ above the
allowed ceiling in $\Theta$, three orders in $g$, before any
systematic. Because the limit improves as the square root of exposure
and grasp, closing the gap would need $10^{11}$ times more of either;
no schedule, aperture or lifetime choice does that. The contract's
dispositions: **Continue** fails; **Revise** holds if the spectral
identifiability result, the line-as-carrier finding and the confounder
ranking are the publishable method; **Redirect** otherwise. The
mentor chose Revise ([[../decisions]] D31).

## Close

The chain from the interaction term to a limit is complete, each block
independently derived and checked, and it answers the gate: no
benchmark allowed by current bounds produces a detectable DarkNESS
signal, by five to six orders of magnitude in $\Theta$. What the
derivation adds beyond that number is the shape of the search: the
information is spectral, the line carries it, and the time-domain
confounders cost 5 % with the spectrum and 94 % without it. Left
explicit: the NXB level and the GRXE model are placeholders that move
$\Theta_{\rm UL}$ by 4×, $f_{\rm live}$ and $\epsilon_{\rm sel}$ are
not yet time-dependent nuisance terms, and the occulted-frame kernel
ends at a constant 150 km shell (D32, Q23).

## Links

- contract §4 and gate: [[detection-channel-derivation-contract]]
- method: [[../03-sensitivity/method]]
- open: [[../open-questions]] Q7, Q14, Q22, Q23
