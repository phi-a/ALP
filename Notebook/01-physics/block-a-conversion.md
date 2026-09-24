---
type: derivation
tags: [darkness, alp, physics, derivation, conversion, block-a]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Block A — ALP-to-photon conversion in the geomagnetic field

Independent derivation, from the interaction term to the kernel the
code computes. Sources by key in [[../references]]; starting equations
in [[derivation-sources]]. `[Yam20]` is compared at the end only.

## Result

For an ALP of energy $E$ entering the detector along $-\hat n$, with
the field sampled along the outward ray $\mathbf r(s) = \mathbf r_{\rm sc}
+ s\hat n$,

$$
P_{a\to\gamma}(E,\hat n,t) = \left(\frac{g}{2}\right)^2
\left|\int_0^{L}\mathbf B_\perp(s)\,e^{iqs}\,ds\right|^2
\equiv \left(\frac{g}{2}\right)^2 K,
\qquad
q = \frac{m_a^2 - \omega_{\rm pl}^2}{2E},
$$

$\mathbf B_\perp = \mathbf B - (\mathbf B\cdot\hat n)\hat n$ a vector,
$L$ the Earth surface for occulted rays and 10 $R_E$ otherwise. In SI
at the interface,

$$
P = 2.45\times10^{-21}
\left(\frac{g}{10^{-10}\ {\rm GeV^{-1}}}\right)^2
\left(\frac{\sqrt K}{\rm T\,m}\right)^2 .
$$

Code: `geometry.transverse_amplitude` (the integral),
`geometry.los_field_integral` (IGRF along a ray),
`geometry.conversion_probability` (the units).

## 1. From the interaction to the mixing equations

Start from `[RS88]`:

$$
\mathcal L = -\tfrac14 F_{\mu\nu}F^{\mu\nu} + \tfrac12(\partial a)^2
- \tfrac12 m_a^2 a^2 - \tfrac14\, g\, a\,F_{\mu\nu}\tilde F^{\mu\nu},
\qquad
-\tfrac14 F\tilde F = \mathbf E\cdot\mathbf B .
$$

Vary $a$ and $\mathbf A$ (temporal gauge, $A_0 = 0$). Linearise about a
static background $\mathbf B_0$ with a wave field $\mathbf A$, keeping
terms first order in the wave and in $g$; add the plasma term for the
photon:

$$
(\Box + m_a^2)\,a = -g\,\dot{\mathbf A}\cdot\mathbf B_0,
\qquad
(\Box + \omega_{\rm pl}^2)\,\mathbf A = g\,\dot a\,\mathbf B_0 .
$$

The wave is longitudinal-free and $\mathbf A\cdot\mathbf B_0$ picks out
the transverse components. Take a plane wave $e^{-i\omega t}$ along
$z$, so only $B_{0x}, B_{0y} \equiv B_x, B_y$ enter (`[Mar22]` eq 3):

$$
(\omega^2 + \partial_z^2 - m_a^2)\,a = i g\omega\,(A_xB_x + A_yB_y),
\qquad
(\omega^2 + \partial_z^2 - \omega_{\rm pl}^2)\,A_j = -i g\omega\,a\,B_j .
$$

Relativistic reduction: $\omega^2 + \partial_z^2 = (\omega + i\partial_z)
(\omega - i\partial_z) \simeq 2\omega(\omega - i\partial_z)$ for a wave
whose envelope changes slowly over a wavelength (`[Mar22]` eq 4). With
$a \to -ia$ the system is Schrödinger-like in $z$:

$$
i\partial_z\Psi = -(H_0 + H_I)\Psi,\quad
\Psi = (A_x, A_y, a)^T,\quad
H_0 = {\rm diag}(\Delta_{\rm pl},\Delta_{\rm pl},\Delta_a),\quad
H_I = \begin{pmatrix}0&0&\Delta_x\\0&0&\Delta_y\\\Delta_x&\Delta_y&0\end{pmatrix},
$$

$$
\Delta_a = -\frac{m_a^2}{2\omega},\qquad
\Delta_{\rm pl} = -\frac{\omega_{\rm pl}^2}{2\omega},\qquad
\Delta_j = \frac{g B_j}{2}\quad (j = x, y).
$$

(`[Mar22]` eq 7–8, which is `[RS88]` in the relativistic limit.)

## 2. First-order amplitude

Treat $H_I$ as a perturbation (justified in §3). In the interaction
picture the amplitude to go from $a$ at $z = 0$ to photon polarisation
$j$ at $z = L$ is, to first order,

$$
\mathcal A_j = -i\int_0^{L} ds\;\Delta_j(s)\;
\exp\!\Big[i\!\int_0^{s}(\Delta_a - \Delta_{\rm pl})\,ds'\Big]
= -\frac{ig}{2}\int_0^{L} ds\;B_j(s)\,e^{-iqs},
$$

$q$ as defined above, taken constant along the ray (§3, plasma). The
two polarisations are incoherent and orthogonal, so

$$
P = |\mathcal A_x|^2 + |\mathcal A_y|^2
= \left(\frac g2\right)^2
\left|\int_0^{L}\mathbf B_\perp(s)\,e^{-iqs}\,ds\right|^2 .
$$

The sign of the phase does not matter: $\mathbf B_\perp$ is real, so
$e^{-iqs}$ gives the complex conjugate of $e^{+iqs}$ and the same
modulus. The basis $(x, y)$ does not matter: the sum of squares is the
squared norm of a transverse vector integral, invariant under
rotations about $\hat n$. What does matter is integrating the
**vector**: if $\mathbf B_\perp$ rotates along the ray the components
partly cancel, and $\int|\mathbf B_\perp|\,ds$ overstates $|\mathcal A|$.

## 3. Validity, one assumption at a time

| Assumption | Number for DarkNESS | Verdict |
|---|---|---|
| Weak mixing (first order in $g$) | $P \le 10^{-16}$ | exact for our purposes |
| Relativistic ($\omega \gg m_a$) | keV against $\le 10^{-5}$ eV | exact |
| Slowly varying envelope | field scale $\sim R_E$ against $\lambda \sim 10^{-10}$ m | exact |
| No absorption along the ray | keV X-rays: free above ~150 km (`[DH06]` §2) | holds for sky rays; see Q23 for occulted rays |
| Plasma term | $n_e \le 10^6$ cm⁻³ → $\omega_{\rm pl} \le 3.7\times10^{-8}$ eV; $\omega_{\rm pl}^2 L/2E \le 2\times10^{-4}$ at 1 keV, 10 $R_E$ | drop; $q = m_a^2/2E$ |
| QED birefringence | $\Delta_{\rm QED}/\omega = \tfrac{7\alpha}{90\pi}(B/B_{\rm crit})^2 = 8\times10^{-33}$ at 30 µT | drop |
| Faraday rotation | $\propto 1/\omega$; negligible at keV (`[Mar22]` fn 2) | drop |
| Field model | IGRF-14 to degree 13, internal only | external magnetosphere separate (Q16) |
| Photon direction | collinear with the ALP (plane wave, $g$ first order) | fixes the ray geometry below |

Each row is a switch the derivation can flip on its own, as the
contract asks.

## 4. Ray geometry

- **Which rays.** The photon keeps the ALP's direction, so the detector
  sees only conversions along lines of sight inside the aperture cone.
  `[RT15]` used the same fact to reject `[Fra14]`: solar ALPs are a
  point source that XMM never looks at. Our source fills the sky, so
  every cone direction carries signal.
- **Orientation.** The ALP travels inward; the code integrates
  outward from the spacecraft. Reversing the path multiplies
  $\mathcal A$ by a phase ($s \to L - s$), leaving $P$ unchanged.
- **Outer end.** 10 $R_E$, where the dipole is $10^{-3}$ of its
  surface value; the truncation costs ~1 % (Q18).
- **Inner end, occulted rays.** The Earth stops photons, and ALPs
  converted beyond it never arrive, so the integral stops at the
  surface (`geometry.path_end_km`). Strictly it should stop at the
  altitude where the atmosphere becomes opaque to keV X-rays, about
  150 km. For a nadir ray at 420 km that is 270 km of path instead of
  420: $\sqrt K$ falls 36 %, $K$ 60 %. It matters only for the
  night-Earth $K$-off frames. **New: Q23.**
- **Aperture.** Average $K$ over the 20° cone with the 19-ray
  quadrature; ray 0 is the boresight
  ([[../2026-09-23-fov-field-integral]]).

## 5. Units

Natural Heaviside–Lorentz units inside; SI at the interface.

| | |
|---|---|
| 1 T | $195.35$ eV² (from $B^2/2\mu_0$ as an energy density) |
| 1 m | $5.0677\times10^6$ eV⁻¹ ($1/\hbar c$) |
| 1 T m | $9.900\times10^8$ eV |
| $g = 10^{-10}$ GeV⁻¹ | $10^{-19}$ eV⁻¹ |

$P = (g\,\sqrt K/2)^2$ with $\sqrt K = 100$ T m and $g = 10^{-10}$
GeV⁻¹ gives $(10^{-19}\times9.9\times10^{10}/2)^2 = 2.45\times10^{-17}$.
`geometry.conversion_probability` carries these two constants
(`constants.EV2_PER_TESLA`, `constants.INV_EV_PER_M`).

## 6. Checks

| # | Check | Test | Result |
|---|---|---|---|
| 1 | Uniform $B_\perp$ over $L$: $K = (B_\perp L)^2\,2(1-\cos qL)/(qL)^2$ | `test_uniform_field_gives_sinc_squared` | agrees to $10^{-5}$ at $qL = 3$ |
| 1b | $q \to 0$: $K \to (B_\perp L)^2$ | `test_zero_phase_is_the_plain_integral` | $10^{-9}$ |
| 2 | $P(100\ {\rm T\,m}, 10^{-10}\ {\rm GeV^{-1}}) = 2.45\times10^{-17}$ | `test_conversion_probability_matches_yamamoto` | 2.4502 |
| 3 | $\mathbf B_\perp \to -\mathbf B_\perp$ at $L/2$: amplitude peaks at $B_\perp L/2$ then cancels | `test_reversed_field_cancels` | residual $< 10^{-2}$ |
| 3b | field along $\hat n$ contributes nothing | `test_field_along_the_ray_does_not_count` | 0 |
| 4 | Rotate field and ray together: $K$ unchanged | `test_rotating_the_frame_leaves_the_amplitude` | $10^{-9}$ |
| 5 | Suzaku orbit, IGRF: $K = 10^4$–$10^5$ T² m² | `test_suzaku_like_geometry_matches_yamamoto` | median in range |
| 6 | Limb ray, 100 vs 800 steps | `test_step_count_converges_on_a_limb_ray` | $< 1\,\%$ |
| 6b | Outer radius 10 vs 20 $R_E$ | `test_outer_radius_converges` | $> 98\,\%$ |
| — | Linear in the field; ray order irrelevant | `test_integral_is_linear_in_the_field`, `test_amplitude_does_not_depend_on_the_ray_ordering` | pass |
| — | Dipole zenith and nadir closed forms | `test_zenith_and_nadir_closed_forms` | 1 % |

All in `tests/test_geometry_los.py`, `test_validation_gates.py`,
`test_invariants.py`.

## 7. Against `[Yam20]`

| `[Yam20]` | Ours | Agree |
|---|---|---|
| eq 2.7, $P = \lvert\tfrac{g}{2}\int B_\perp e^{-iqs}ds\rvert^2$ with $B_\perp$ scalar ($\mathbf B\times\hat e_a$ magnitude) | vector $\mathbf B_\perp$ | same when the transverse direction is fixed; ours is smaller when it rotates |
| eq 2.9, $q = m_a^2/2E$ | same, plasma dropped with a number | yes |
| eq 2.10, uniform field | check 1 | yes |
| eq 2.13, $2.45\times10^{-21}$ | check 2 | yes |
| §3.1, IGRF to 6 $R_E$, $K \sim 10^4$–$10^5$ | 10 $R_E$; check 5 | yes |
| eq 2.12 coherence, $m_a < \sqrt{2E/L}$ | same form; the knee from our own $L$ ([[coherence-and-mass-reach]]) | text value not inherited |

## What the student's Block A must contain

The mixing equations from the Lagrangian; the first-order amplitude
with the phase inside the integral; a statement of which of the §3
assumptions are made and the number behind each; the ray orientation
and both endpoints; the T m → eV conversion; and the six checks with
their numbers. Compare check by check before comparing derivations.

## Links

- contract §2: [[detection-channel-derivation-contract]]
- kernel in the mission model: [[../02-mission-analysis/geomagnetic-integral]]
- next: Block B, the source
