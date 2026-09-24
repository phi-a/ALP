---
type: derivation
tags: [darkness, alp, physics, derivation, conversion, block-a]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Block A — ALP-to-photon conversion in the geomagnetic field

This note derives the conversion probability for one DarkNESS line of
sight from the interaction term, gives each assumption its number,
fixes the ray geometry and the units, and checks the result against
closed forms and against `[Yam20]`. Keys refer to [[../references]];
starting equations are in [[derivation-sources]].

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

with $\mathbf B_\perp = \mathbf B - (\mathbf B\cdot\hat n)\hat n$ a
vector and $L$ the entry into the 150 km opaque-air shell, or 10 $R_E$
if the ray never enters it. In SI
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

`[RS88]`:

$$
\mathcal L = -\tfrac14 F_{\mu\nu}F^{\mu\nu} + \tfrac12(\partial a)^2
- \tfrac12 m_a^2 a^2 - \tfrac14\, g\, a\,F_{\mu\nu}\tilde F^{\mu\nu},
\qquad
-\tfrac14 F\tilde F = \mathbf E\cdot\mathbf B .
$$

Varying $a$ and $\mathbf A$ (temporal gauge, $A_0 = 0$), linearising
about a static background $\mathbf B_0$ with a wave field $\mathbf A$
to first order in the wave and in $g$, and adding the plasma term for
the photon:

$$
(\Box + m_a^2)\,a = -g\,\dot{\mathbf A}\cdot\mathbf B_0,
\qquad
(\Box + \omega_{\rm pl}^2)\,\mathbf A = g\,\dot a\,\mathbf B_0 .
$$

For a plane wave $e^{-i\omega t}$ along $z$ only the transverse
components $B_x, B_y$ of $\mathbf B_0$ enter (`[Mar22]` eq 3):

$$
(\omega^2 + \partial_z^2 - m_a^2)\,a = i g\omega\,(A_xB_x + A_yB_y),
\qquad
(\omega^2 + \partial_z^2 - \omega_{\rm pl}^2)\,A_j = -i g\omega\,a\,B_j .
$$

For an envelope that changes slowly over a wavelength,
$\omega^2 + \partial_z^2 = (\omega + i\partial_z)(\omega - i\partial_z)
\simeq 2\omega(\omega - i\partial_z)$ (`[Mar22]` eq 4). With
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
\Delta_j = \frac{g B_j}{2}\quad (j = x, y),
$$

which is `[RS88]` in the relativistic limit (`[Mar22]` eq 7–8).

## 2. First-order amplitude

With $H_I$ a perturbation (§3), the amplitude from $a$ at $z = 0$ to
photon polarisation $j$ at $z = L$ is, to first order,

$$
\mathcal A_j = -i\int_0^{L} ds\;\Delta_j(s)\;
\exp\!\Big[i\!\int_0^{s}(\Delta_a - \Delta_{\rm pl})\,ds'\Big]
= -\frac{ig}{2}\int_0^{L} ds\;B_j(s)\,e^{-iqs},
$$

$q$ constant along the ray (§3, plasma). The two polarisations are
orthogonal and add incoherently:

$$
P = |\mathcal A_x|^2 + |\mathcal A_y|^2
= \left(\frac g2\right)^2
\left|\int_0^{L}\mathbf B_\perp(s)\,e^{-iqs}\,ds\right|^2 .
$$

The sign of the phase does not matter: $\mathbf B_\perp$ is real, so
$e^{-iqs}$ gives the complex conjugate and the same modulus. The
transverse basis does not matter: the sum of squares is the squared
norm of a vector integral, invariant under rotation about $\hat n$.
The vector does matter: where $\mathbf B_\perp$ rotates along the ray
the components partly cancel, and $\int|\mathbf B_\perp|\,ds$
overstates $|\mathcal A|$.

## 3. Validity, one assumption at a time

| Assumption | Number for DarkNESS | Verdict |
|---|---|---|
| Weak mixing (first order in $g$) | $P \le 10^{-16}$ | exact for our purposes |
| Relativistic ($\omega \gg m_a$) | keV against $\le 10^{-5}$ eV | exact |
| Slowly varying envelope | field scale $\sim R_E$ against $\lambda \sim 10^{-10}$ m | exact |
| No absorption along the ray | keV X-rays free above ~150 km (`[DH06]` §2) | rays end at the 150 km shell, §4 (D32) |
| Plasma term | $n_e \le 10^6$ cm⁻³ → $\omega_{\rm pl} \le 3.7\times10^{-8}$ eV; $\omega_{\rm pl}^2 L/2E \le 2\times10^{-4}$ at 1 keV, 10 $R_E$ | drop; $q = m_a^2/2E$ |
| QED birefringence | $\Delta_{\rm QED}/\omega = \tfrac{7\alpha}{90\pi}(B/B_{\rm crit})^2 = 8\times10^{-33}$ at 30 µT | drop |
| Faraday rotation | $\propto 1/\omega$; negligible at keV (`[Mar22]` fn 2) | drop |
| Field model | IGRF-14 to degree 13, internal only | external magnetosphere separate (Q16) |
| Photon direction | collinear with the ALP (plane wave, first order in $g$) | fixes §4 |

## 4. Ray geometry

- **Which rays.** The photon keeps the ALP's direction, so the detector
  sees only conversions along lines of sight inside the aperture cone.
  `[RT15]` rejected `[Fra14]` on this fact: solar ALPs are a point
  source that XMM never looks at. Our source fills the sky, so every
  cone direction carries signal.
- **Orientation.** The ALP travels inward; the code integrates outward
  from the spacecraft. Reversing the path ($s \to L - s$) multiplies
  $\mathcal A$ by a phase and leaves $P$ unchanged.
- **Outer end.** 10 $R_E$, where the dipole is $10^{-3}$ of its
  surface value; truncation costs ~1 % (Q18).
- **Inner end.** A photon converted below the altitude where air is
  opaque to keV X-rays never arrives, and ALPs converted beyond the
  Earth do not either, so a ray ends at its first entry into the
  150 km shell (`geometry.path_end_km`, D32). Against a ground end
  that lowers $K$ of occulted frames to a median 0.37 (range
  0.17–0.43) on the reference day, and a nadir ray at 420 km to 0.39
  ([[../2026-09-24-occulted-ray-endpoint]]). The shell altitude is a
  constant where the truth rises with nadir angle and falls with
  energy (Q23). Sky rays are unaffected.
- **Aperture.** $K$ averaged over the 20° cone with the 19-ray
  quadrature, ray 0 the boresight
  ([[../2026-09-23-fov-field-integral]]).

## 5. Units

Natural Heaviside–Lorentz units inside; SI at the interface.

| | |
|---|---|
| 1 T | $195.35$ eV² (from $B^2/2\mu_0$ as an energy density) |
| 1 m | $5.0677\times10^6$ eV⁻¹ ($1/\hbar c$) |
| 1 T m | $9.900\times10^8$ eV |
| $g = 10^{-10}$ GeV⁻¹ | $10^{-19}$ eV⁻¹ |

$\sqrt K = 100$ T m and $g = 10^{-10}$ GeV⁻¹ give
$P = (10^{-19}\times9.9\times10^{10}/2)^2 = 2.45\times10^{-17}$.
`geometry.conversion_probability` carries the two constants
(`constants.EV2_PER_TESLA`, `constants.INV_EV_PER_M`).

## 6. Checks

| # | Check | Test | Result |
|---|---|---|---|
| 1 | Uniform $B_\perp$ over $L$: $K = (B_\perp L)^2\,2(1-\cos qL)/(qL)^2$ | `test_uniform_field_gives_sinc_squared` | agrees to $10^{-5}$ at $qL = 3$ |
| 1b | $q \to 0$: $K \to (B_\perp L)^2$ | `test_zero_phase_is_the_plain_integral` | $10^{-9}$ |
| 2 | $P(100\ {\rm T\,m}, 10^{-10}\ {\rm GeV^{-1}}) = 2.45\times10^{-17}$ | `test_conversion_probability_matches_yamamoto` | 2.4502 |
| 3 | $\mathbf B_\perp \to -\mathbf B_\perp$ at $L/2$: amplitude peaks at $B_\perp L/2$, then cancels | `test_reversed_field_cancels` | residual $< 10^{-2}$ |
| 3b | Field along $\hat n$ contributes nothing | `test_field_along_the_ray_does_not_count` | 0 |
| 4 | Rotate field and ray together: $K$ unchanged | `test_rotating_the_frame_leaves_the_amplitude` | $10^{-9}$ |
| 5 | Suzaku orbit, IGRF: $K = 10^4$–$10^5$ T² m² | `test_suzaku_like_geometry_matches_yamamoto` | median in range |
| 6 | Limb ray, 100 against 800 steps | `test_step_count_converges_on_a_limb_ray` | $< 1\,\%$ |
| 6b | Outer radius 10 against 20 $R_E$ | `test_outer_radius_converges` | $> 98\,\%$ |
| — | Linear in the field; ray order irrelevant | `test_integral_is_linear_in_the_field`, `test_amplitude_does_not_depend_on_the_ray_ordering` | pass |
| — | Dipole zenith and nadir closed forms | `test_zenith_and_nadir_closed_forms` | 1 % |

In `tests/test_geometry_los.py`, `test_validation_gates.py`,
`test_invariants.py`.

## 7. Against `[Yam20]`

| `[Yam20]` | Ours | Agree |
|---|---|---|
| eq 2.7, $P = \lvert\tfrac{g}{2}\int B_\perp e^{-iqs}ds\rvert^2$, $B_\perp$ the magnitude of $\mathbf B\times\hat e_a$ | vector $\mathbf B_\perp$ | same when the transverse direction is fixed; ours smaller when it rotates |
| eq 2.9, $q = m_a^2/2E$ | same, plasma dropped with a number | yes |
| eq 2.10, uniform field | check 1 | yes |
| eq 2.13, $2.45\times10^{-21}$ | check 2 | yes |
| §3.1, IGRF to 6 $R_E$, $K \sim 10^4$–$10^5$ | 10 $R_E$; check 5 | yes |
| eq 2.12 coherence, $m_a < \sqrt{2E/L}$ | same form, knee from our own $L$ ([[coherence-and-mass-reach]]) | form yes; their text value not inherited |

## Close

The conversion probability for a sky ray is derived, checked, and
agrees with `[Yam20]` wherever the transverse field keeps its
direction; where it rotates, the vector integral is the correct and
smaller one. Block A is closed. The one declared approximation is the
constant 150 km end of a ray (D32, Q23), which touches only the
night-Earth control frames.

## Links

- contract §2: [[detection-channel-derivation-contract]]
- kernel in the mission model: [[../02-mission-analysis/geomagnetic-integral]]
- next: Block B, the source
