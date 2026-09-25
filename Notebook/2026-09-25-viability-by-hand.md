---
type: derivation
tags: [darkness, alp, viability, gate, closed-form, envelope]
created: 2026-09-25
updated: 2026-09-25
status: active
---

# 2026-09-25 — the viability gate by hand

Block D answered the gate with the full chain and a Fisher matrix
([[01-physics/block-d-claim]] §5). This note answers it again with
nothing but published bounds, four constants and arithmetic, so that
the conclusion does not rest on the pipeline. Every number carries its
source; the last section compares the two routes. Keys refer to
[[references]].

## Obligation

Show, without the state table or the likelihood code, whether any
$\chi\to aa$ model allowed by current bounds gives a DarkNESS count
the mission could see, and bound how much the unfinished analysis
items can change that.

## 1. The ceiling

The converted brightness is proportional to $\Theta = g^2 f/\tau$
(Blocks A, B). The two factors are bounded separately:

| Bound | Value | Source |
|---|---|---|
| $g$ | $< 0.47\times10^{-10}$ GeV⁻¹ | globular clusters, `[DHV22]` |
| $f/\tau$ | $< 4.0\times10^{-3}$ Gyr⁻¹ | Planck 2018, dark matter → dark radiation, `[NTH21]` |

$$
\Theta_{\max} = (0.47\times10^{-10})^2\times4.0\times10^{-3}
= 8.8\times10^{-24}\ {\rm GeV^{-2}\,Gyr^{-1}} .
$$

Both are the loosest defensible choices. For ALP masses below the
coherence knee ($m_a \lesssim 10^{-5}$ eV, [[01-physics/coherence-and-mass-reach]])
no bound on $g$ is weaker than the stellar one; below $10^{-12}$ eV
the cluster X-ray bounds are 100× tighter. The DES-Y1 bound on all of
the dark matter, $\tau > 50$ Gyr (`[DES21]`), would loosen $f/\tau$
by 5×; §5 carries that as a row.

## 2. Source at Earth

The line carries the search (Block D), so the envelope is the line.
For a 7 keV parent, $E_0 = 3.5$ keV, and

$$
I_{\rm line} = \frac{f}{\tau}\,\frac{D}{2\pi m_\chi} .
$$

$D$ along the Galactic Centre, cone-averaged over the 20° aperture,
is $1.27\times10^{23}$ GeV cm⁻² (Block C: $\sum\Delta t\langle DK\rangle
/ \sum\Delta t\langle K\rangle$; the boresight value from
`source.column_density(0, 0)` is $1.99\times10^{23}$, the full-sky
mean $2.1\times10^{22}$). With $4.0\times10^{-3}$ Gyr⁻¹ $=
1.27\times10^{-19}$ s⁻¹:

$$
I_{\rm line} = \frac{1.27\times10^{-19}\ {\rm s^{-1}}\times
1.27\times10^{23}\ {\rm GeV\,cm^{-2}}}{2\pi\times7\times10^{-6}\ {\rm GeV}}
= 3.7\times10^{8}\ {\rm cm^{-2}\,s^{-1}\,sr^{-1}} .
$$

That is the ALP flux. It is large; what follows is small.

## 3. Conversion

Block A, in `[Yam20]`'s units:
$P = 2.45\times10^{-21}\,(g/10^{-10})^2\,K$, $K$ in T² m². At
$g_{\max}$, $P = 5.4\times10^{-22}\,K$. The reference schedule's
time-weighted mean kernel is $K = 1.95\times10^{8}/23\,400 = 8.3\times
10^{3}$ T² m² ($\sqrt K = 91$ T m; Block C), so

$$
P = 4.5\times10^{-18} .
$$

Envelope on $K$ for any pointing from 420 km: along a ray the dipole
field is at most $2B_0(R_E/r)^3$ and the longest path at low $r$ is
the tangent ray, $\int_0^\infty (r_0^2+s^2)^{-3/2}ds = 1/r_0^2$, so

$$
\sqrt K \le 2B_0R_E\Big(\frac{R_E}{r_0}\Big)^2 = 3.3\times10^{2}\ {\rm T\,m},
\qquad K \le 1.1\times10^{5}\ {\rm T^2\,m^2},
$$

with $B_0 R_E/2 = 95$ T m (`test_hand_calculation_of_the_surface_integral`).
The reference day sits within 13× of the largest kernel any pointing
can reach, and the limb-grazing maximum of
[[02-mission-analysis/pointing-optimization]] is below this bound.

## 4. Counts

Grasp $A\Omega = 12\ {\rm cm^2}\times0.0955\ {\rm sr} = 1.15$ cm² sr,
live fraction 0.5, QE ≈ 1 at 3.5 keV (Block C), 23 400 s of science
per reference day:

$$
S_{\rm day} = 3.7\times10^{8}\times4.5\times10^{-18}\times1.15\times0.5
\times2.34\times10^{4} = 2.2\times10^{-5}\ {\rm counts} .
$$

Over the 187-day science phase, $S = 4.1\times10^{-3}$ counts. The
continuum adds 10 % (ceiling refresh: $2.5\times10^{-4}$ over 187 days
at $\Theta_{\max}$). Not one photon.

## 5. Background under the line

The line is a delta at the detector, spread by the 151 eV FWHM at
3.5 keV (`detector.resolution_fwhm_kev`); a $\pm1\sigma$ window is
$w = 0.128$ keV. CXB in the cone (`[DLM04]`, $11.6\,E^{-1.41}$):
19.8 counts s⁻¹ over 1–10 keV before masking, 9.9 after. The share
in the window is $11.6\times3.5^{-1.41}\times w / 17.3 = 1.5\,\%$, so
$3.4\times10^{3}$ counts per day; the flat particle proxy at the same
level adds $3.3\times10^{3}$. Over 187 days,

$$
B = 1.25\times10^{6}\ {\rm counts\ under\ the\ line} .
$$

The Galactic ridge, 27× CXB on the Centre, is left out: it only
raises $B$.

## 6. The gate

A 90 % one-sided limit with the background known needs
$S \ge 1.28\sqrt B = 1.4\times10^{3}$ counts. The allowed ceiling gives
$4.1\times10^{-3}$:

$$
\frac{\Theta_{\rm UL}}{\Theta_{\max}} = \frac{1.4\times10^{3}}{4.1\times10^{-3}}
= 3.5\times10^{5} .
$$

$S$ and $B$ both scale with grasp × time, so the ratio falls as
$(A\Omega\,T)^{-1/2}$; closing it needs $(3.5\times10^{5})^2 =
1.2\times10^{11}$ times the reference exposure-grasp of
$5.0\times10^{6}$ cm² sr s, i.e. $6\times10^{17}$ cm² sr s: one square
metre steradian for twenty million years. Written for any instrument,

$$
\frac{\Theta_{\rm UL}}{\Theta_{\max}} =
\frac{1.28\sqrt{b\,w}}{I_{\rm line}(\Theta_{\max})\,P(\Theta_{\max},K)}
\,\frac{1}{\sqrt{A\Omega\,T f_{\rm live}}},
$$

$b$ the background brightness per keV under the line. The only levers
are $K$ (bounded, §3), $w$ (resolution) and exposure-grasp.

## 7. What the unfinished items can buy

Each open item, taken at its most favourable, and its effect on the
ratio:

| Item | Best case | Gain in $\Theta_{\rm UL}/\Theta_{\max}$ |
|---|---|---|
| Pointing optimisation (not computed) | every sample at the §3 bound | ≤ 13 |
| Sunlit observing (Q5) | duty cycle ×2 | 1.4 |
| Sensor area (Q2) | 12 cm² is already the larger value | 1 (0.8 if 8 cm²) |
| Orbit case (Q3) | contained in the §3 bound | 1 |
| Particle level (Q7, `ASSUME`) | zero | 1.4 |
| Ridge model | already excluded | 1 |
| Decay bound | DES-Y1 in place of Planck | 5 |
| Resolution | 5 eV microcalorimeter, not a CCD | 5.5 |
| Suzaku 85× normalisation question | resolves in our favour | ≤ 85 |

Stacked for DarkNESS as built (first five rows): 13 × 1.4 × 1.4 = 25,
leaving $1.4\times10^{4}$. Stacked with the looser decay bound and a
calorimeter: $\times 28$ more, leaving $5\times10^{2}$. Only the last
row is a real unknown rather than a bounded trade, and even granted in
full it leaves a factor of 6 on top of everything else. No combination
reaches 1.

## 8. Against the pipeline

| Quantity | By hand | Block D | Route |
|---|---|---|---|
| $\Theta_{\max}$ | $8.8\times10^{-24}$ | $8.8\times10^{-24}$ | same inputs |
| line counts, reference day | $2.2\times10^{-5}$ | $2.2\times10^{-5}$ | 39-sample state table |
| background, reference day | $4.6\times10^{5}$ (all band) | $4.5\times10^{5}$ | templates |
| $\Theta_{\rm UL}/\Theta_{\max}$ | $3.5\times10^{5}$ | $3.8\times10^{5}$ | 36-bin Fisher, 4 nuisances |

The two routes agree to 10 %. The Fisher machinery loses 5 % to
profiling and gains a little from the wings of the line and the
continuum; the envelope has neither. Test:
`test_viability_gate_by_hand` in `tests/test_validation_gates.py`.

## 9. The allowed-region map

Would a map of $\Theta_{\max}$ against $(m_\chi, m_a)$ with the reach
drawn on it add anything? $\Theta_{\max}$ is flat in $m_\chi$ (neither
bound depends on the parent mass) and flat in $m_a$ below the
coherence knee. The reach moves with $m_\chi$ only through QE, the
resolution and the background slope at $E_0$: over 2–20 keV that is
a factor of 3 in the ratio, and above the knee the ratio only grows.
The map is one number, $3\times10^{5}$, with a roll-off at
$m_a\sim10^{-5}$ eV. It is worth one panel of the paper's existing
ceiling figure (`conops.ipynb` figure 6, reach and ceiling against
$m_\chi$), not a figure of its own and not a paper.

## Close

Bounds on $g$ and on decaying dark matter, the halo column, the
geomagnetic kernel and the cosmic X-ray background fix the answer
without the pipeline: $4\times10^{-3}$ signal counts on $10^{6}$
background under the line, a gap of $3.5\times10^{5}$ in $\Theta$ that
the unfinished items can shrink by at most $10^{2}$–$10^{3}$. The
pipeline gives $3.8\times10^{5}$ by an independent route. What stays
open is not the gate but its provenance: Q19, whether `[DMR21]` or
Cui et al. 2022 (paper key `cui2022cosmogenic`) already state the
ceiling.

## Links

- decision: [[decisions]] D31
- full chain: [[01-physics/block-d-claim]]
- result prose: [[03-sensitivity/result]]
- open: [[open-questions]] Q14, Q19
