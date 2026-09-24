---
type: note
tags: [darkness, alp, physics, derivation, sources, notation]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Derivation sources and notation

Step 1 of the independent derivation
([[detection-channel-derivation-contract]]): for each block, the
origin equation we start from, the DarkNESS inputs, and the checks.
Keys refer to [[../references]]. Yamamoto `[Yam20]` is a benchmark
to reproduce at the end, never a starting equation.

## Rules

- Derive from the origin papers below. Do not read `[Yam20]` §2 until
  the block is done; then compare.
- Every symbol appears in the notation table. Natural units
  ($\hbar = c = 1$, Heaviside–Lorentz) inside the derivation; SI at
  the interfaces, with the conversion written out.
- Each block ends with its analytic checks and a script that runs
  them.

## Notation

| Ours | Meaning | `[DMR21]` | `[Yam20]` | `[Mar22]` / `[DH06]` |
|---|---|---|---|---|
| $m_\chi$ | parent mass | $m$ | $m_\phi$ | — |
| $\tau$, $\Gamma = 1/\tau$ | parent lifetime, rate | $\tau$, $\Gamma$ | $\Gamma_{2a}$ | — |
| $f_\chi$ | parent share of DM today | — | — | — |
| $\mathcal B_{aa}$ | branching to $aa$ | — | — | — |
| $E$, $E_0 = m_\chi/2$ | ALP energy, line energy | $\omega$, $m/2$ | $E_a$, $m_\phi/2$ | $\omega$ |
| $g$ | $g_{a\gamma\gamma}$ | $g_{a\gamma}$ | $g_{a\gamma}$ | $g_{a\gamma}$ / $1/M$ |
| $m_a$ | ALP mass | $m_a$ | $m_a$ | $m_a$ |
| $\omega_{\rm pl}$ | plasma frequency | — | — | $\omega_{\rm pl}$ / $m_\gamma$ |
| $D(\hat n) = \int\rho_\chi\,ds$ | halo column | D-factor | $S$ | — |
| $\mathbf B_\perp$ | field transverse to the ray (vector) | — | $B_\perp$ (scalar) | $B_x, B_y$ |
| $q = (m_a^2 - \omega_{\rm pl}^2)/2E$ | momentum transfer | — | $m_a^2/2E_a$ | $\Delta_{\rm pl} - \Delta_a$ / $q$ |
| $\mathcal A$ | $\int \mathbf B_\perp e^{iqs}ds$ (T m) | — | — | $A_{x\to a}$ |
| $K = \lvert\mathcal A\rvert^2$ | conversion kernel (T² m²) | — | $(B_\perp L)^2$ | — |
| $P = (g/2)^2 K$ | conversion probability | — | $P_{a\gamma}$ | $P$ / $p(L)$ |
| $\Theta = g^2 f_\chi\mathcal B_{aa}/\tau$ | the measurable product | — | — | — |

## Block A — conversion in the geomagnetic field

**Origin.** The linearised ALP–Maxwell system of `[RS88]`, as restated
in `[Mar22]` eq 2. With propagation along $z$ and the rotating-wave
reduction (`[Mar22]` eq 4, 7, 8):

$$
(\omega - i\partial_z)\,a = \frac{m_a^2}{2\omega}\,a
 - \frac{g}{2}\,(A_xB_x + A_yB_y),
\qquad
(\omega - i\partial_z)\,A_j = \frac{\omega_{\rm pl}^2}{2\omega}\,A_j
 - \frac{g B_j}{2}\,a .
$$

To leading order in $g$ (`[Mar22]` eq 17–18, read for $a\to\gamma$):

$$
\mathcal A_j = -i\int_0^{L} ds\,\frac{g B_j(s)}{2}\,
e^{-i\varphi(s)},\qquad
\varphi(s) = \int_0^{s}\frac{\omega_{\rm pl}^2(s') - m_a^2}{2E}\,ds',
\qquad
P = \lvert\mathcal A_x\rvert^2 + \lvert\mathcal A_y\rvert^2 .
$$

Sign conventions for $\varphi$ drop out of $P$. The vector components
$B_x, B_y$ are integrated separately; a scalar $\lvert\mathbf B_\perp\rvert$
integral is wrong when the transverse field rotates along the ray.
`geometry.los_integral` does this correctly;
[[../02-mission-analysis/geomagnetic-integral]] still writes the scalar
form and should be corrected.

**Units.** 1 T = 195.35 eV², 1 m = 5.068×10⁶ eV⁻¹, so
1 T m = 9.90×10⁸ eV. With $g = 10^{-10}$ GeV⁻¹ $= 10^{-19}$ eV⁻¹ and
$B_\perp L = 100$ T m, $P = (g\,B_\perp L/2)^2 = 2.45\times10^{-17}$.
(The 2.6×10⁻¹⁷ in [[alp-signal-chain]] is rounded; use 2.45.)

**DarkNESS inputs.**

| Input | Value | Tag |
|---|---|---|
| Field | IGRF-14, degree 13 `[IGRF14]` | `EXT` |
| Ray | from the spacecraft outward along $\hat n$, to 10 $R_E$ (Q18) | `ASSUME` |
| Aperture | 20° cone, 19-ray equal-area quadrature | `DN-V` / `DERIV` |
| Energy | 1–10 keV | `DN-V` |
| Plasma | $n_e \le 10^6$ cm⁻³ → $\omega_{\rm pl} \le 3.7\times10^{-8}$ eV; $qL \ll 1$ for all $m_a$ of interest (A4) | `DERIV` |
| Absorption | none above 150 km (`[DH06]` §2) | `EXT` |

**Direction rule.** In the weak-mixing plane-wave limit the photon is
collinear with the ALP. `[RT15]` sinks `[Fra14]` on exactly this point:
the Sun is a point source and XMM never points at it. Our source fills
the sky, so the rule works for us instead: the signal comes only from
directions inside the cone, converted only in the field *in front of*
the detector along those rays.

**Checks.**

1. Uniform $B_\perp$ over $L$: $P = (gB_\perp L/2)^2\,
   \dfrac{2(1-\cos qL)}{(qL)^2}$ (`[Yam20]` eq 2.10; `[DH06]` eq 2 with
   absorption off).
2. $g = 10^{-10}$ GeV⁻¹, $B_\perp L = 100$ T m, $q\to0$:
   $P = 2.45\times10^{-17}$ (`[Yam20]` eq 2.13).
3. $B_\perp \to -B_\perp$ halfway along $L$ with $q = 0$: $P = 0$.
4. Rotate the transverse basis: $P$ unchanged.
5. Suzaku orbit and IGRF: $K$ in the range $10^4$–$10^5$ T² m²
   (`[Yam20]` §3.1; already in [[../02-mission-analysis/yamamoto-validation-101002010]]).
6. Step-count convergence on a limb-grazing LEO ray (`test_geometry`).

## Block B — source

**Origin.** Counting, `[DMR21]` eq 5–7. Decays at cosmic time $t$
(scale factor $a$, $a_0 = 1$) of parents with number density
$\rho_\chi(t)/m_\chi$, rate $\Gamma$, survival $e^{-\Gamma t}$, emit
$dN/dE'$ per decay; the energy redshifts, $E = aE'$, and the number
density dilutes by $a^3$. Written with the Jacobian explicit:

$$
\frac{dn_a}{dE} = \int_0^{t_0} dt\; a^3\, e^{-\Gamma t}\,
\frac{\rho_\chi(t)}{m_\chi}\,\Gamma\,
\frac{1}{a}\,\frac{dN}{dE'}\Big|_{E' = E/a},
\qquad
\frac{dN}{dE'} = 2\,\delta(E' - E_0).
$$

With $\rho_\chi(t) = f_\chi\rho_{{\rm DM},0}\,a^{-3}$ before decay,
$dt = da/(aH(a))$ and $\mathcal B_{aa}$ on the rate, the delta function
fixes $a_* = E/E_0$ and gives

$$
\frac{dn_a}{dE} = \frac{2\,f_\chi\mathcal B_{aa}\,\rho_{{\rm DM},0}}
{m_\chi\,\tau}\;
\frac{e^{-t(a_*)/\tau}}{E\,H(a_*)}\;
\Theta(E_0 - E),
\qquad
\frac{d\Phi}{dE\,d\Omega} = \frac{1}{4\pi}\frac{dn_a}{dE}
\quad(c = 1).
$$

`[DMR21]` eq 8 quotes $E\,dn_a/dE$ (energy density per log energy);
that is the form to match. The $1/a$ Jacobian is the factor most
easily lost. $H(a) = H_0\sqrt{\Omega_m a^{-3} + \Omega_\Lambda}$ with
`[Pl18]` values; $t(a)$ from the same.

Milky Way, `[DMR21]` eq 9: decays now ($t = t_U$), per steradian,

$$
\frac{d\Phi}{dE\,d\Omega}(\hat n) = \frac{f_\chi\mathcal B_{aa}}{4\pi m_\chi\tau}\,
\frac{dN}{dE}\,D(\hat n),
\qquad
I_{\rm line}(\hat n) = \frac{f_\chi\mathcal B_{aa}\,D(\hat n)}{2\pi m_\chi\tau}.
$$

Line width: halo dispersion and the Sun's motion, both $v/c\sim10^{-3}$
(`[DMR21]` §II B; `[EOM19]` for the numbers). Before detector smearing.

**Parent fraction.** $f_\chi$ above is the share *today*. If the
student defines a primordial share, the two differ by
$e^{-t_U/\tau}$ and the extragalactic normalisation changes. State
which one is used; the contract requires it.

**DarkNESS inputs.**

| Input | Value | Tag |
|---|---|---|
| Halo | NFW, $r_s = 20$ kpc, $\rho_\odot = 0.4$ GeV cm⁻³, $R_\odot = 8.1$ kpc (`source.halo`) | `EXT` / `ASSUME` |
| Cosmology | `[Pl18]`: $H_0 = 67.4$, $\Omega_m = 0.315$, $\Omega_\Lambda = 0.685$, $\rho_{{\rm DM},0} = 1.26$ keV cm⁻³ | `EXT` |
| Parent | $m_\chi$ = 2–20 keV so $E_0$ sits in the band; 7 keV as the working case | `ASSUME` |

**Checks.**

1. $\int (dn_a/dE)\,dE$ over both components at $\tau \gg t_U$:
   extragalactic and Milky Way energy densities comparable, and
   $\rho_a^{\rm MW}/\rho_a^{\rm EG}$ within the `[DMR21]` statement.
2. Full-sky $\int D\,d\Omega = 2.7\times10^{32}$ eV cm⁻² sr
   (`[DMR21]` footnote 8) from `source.halo`.
3. Continuum has support only at $E \le E_0$; line at $E_0$ with
   fractional width $\sim10^{-3}$.
4. $I_{\rm line}$ matches `[Yam20]` eq 2.2 with $S\to D$,
   $\Gamma_{2a}\to f_\chi\mathcal B_{aa}/\tau$.
5. Continuum matches `[Yam20]` eq 2.5 numerically with the same
   cosmology. Their $f(x)$ (eq 2.6) as printed reads
   $[\Omega_m + (1-\Omega_m-\Omega_\Lambda)/x - \Omega_\Lambda/x^3]^{-1/2}$;
   the Friedmann equation gives $+\Omega_\Lambda/x^3$. Check the
   printed paper before treating the sign as a typo.

## Block C — detector counts

**Origin.** The count integral in the contract §3, with the detector
factors from [[../00-baseline/skipper-ccd]]:

$$
\mu^{\rm sig}_{ij} = \int_{\Delta t_i}dt\int d\Omega\int dE\;
\frac{d\Phi}{dE\,d\Omega}\,P(E,\hat n,t)\,
A_{\rm geo}\,\mathcal V(\theta)\,T_{\rm Al}(E)\,\eta_{\rm Si}(E)\,
\epsilon_{\rm sel}\,f_{\rm live}\,R_j(E).
$$

**DarkNESS inputs.** `[Alp25]`, `[Alp26]`: $A_{\rm geo} = 12$ cm²,
20° cone ($\Omega = 0.0955$ sr), 50 nm Al, 500 µm Si, 169 eV FWHM
(173–198 eV at end of life), $f_{\rm live}\approx0.5$,
$\epsilon_{\rm sel}$ open, 15-min observations, 0.5–1 Ms.

**Checks.** Constant-brightness sky recovers
$I\times1.15\ {\rm cm^2\,sr}\times{\rm QE}\times f_{\rm live}\times T$;
a monochromatic input conserves counts through $R_j$; losses applied
once; cone average tends to the boresight as the half-angle → 0
(ALP-CH-17).

## Block D — allowed parameter space (Q14)

The data constrain $\Theta = g^2 f_\chi\mathcal B_{aa}/\tau$. The
ceiling on $\Theta$ from existing limits:

| Factor | Bound | Source |
|---|---|---|
| $f_\chi\mathcal B_{aa}/\tau$ | $< 4.0\times10^{-3}$ Gyr⁻¹ (Planck 2018); $3.7\times10^{-3}$ with BAO | `[NTH21]` |
| same, older | $< 6.3\times10^{-3}$ Gyr⁻¹ (used in D28) | `[PSL16]` |
| $\tau$, all DM | $> 50$ Gyr | `[DES21]` |
| $g$ | $< 0.66\times10^{-10}$ GeV⁻¹ | `[CAST17]`, `[Aya14]` |
| $g$ | $< 0.47\times10^{-10}$ GeV⁻¹ | `[DHV22]` |

$\Theta_{\max} = (0.47\times10^{-10}\ {\rm GeV^{-1}})^2\times
4.0\times10^{-3}\ {\rm Gyr^{-1}}$. D28 used $g = 5.8\times10^{-11}$ and
$6.3\times10^{-3}$ Gyr⁻¹; the current ceiling is 2.4× lower. The
viability gate is rerun with this $\Theta_{\max}$ once blocks A–C are
independently confirmed.

Prior Earth-field searches to compare against: `[Yam20]` eq 4.1,
$g < 3.3\times10^{-7}$ GeV⁻¹ scaled by $(m_\chi/10\ {\rm keV})^{5/4}
(\tau/4.32\times10^{17}\ {\rm s})^{1/2}(B_\perp L/100\ {\rm T\,m})^{-1}$,
for $m_a < 3.3\times10^{-6}$ eV; `[Fra14]` as a cautionary tale.

## Yamamoto as benchmark

What we reproduce, and only after each block is done:

| `[Yam20]` | Reproduced by |
|---|---|
| eq 2.2, line intensity | Block B check 4 |
| eq 2.5–2.6, continuum | Block B check 5 |
| eq 2.10, 2.13, conversion | Block A checks 1–2 |
| §3.1, $K = 10^4$–$10^5$ T² m² for Suzaku | Block A check 5 |
| eq 4.1, the coupling bound | Block D, with Suzaku's grasp and exposure ([[../03-sensitivity/method]]) |

## Links

- contract: [[detection-channel-derivation-contract]]
- bibliography: [[../references]]
- detector: [[../00-baseline/skipper-ccd]]
- open: [[../open-questions]] Q14, Q15, Q18
