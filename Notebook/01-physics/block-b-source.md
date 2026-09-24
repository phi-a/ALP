---
type: derivation
tags: [darkness, alp, physics, derivation, source, block-b]
created: 2026-09-24
updated: 2026-09-24
status: active
---

# Block B — the ALP source from a decaying parent

This note derives the ALP intensity at Earth from $\chi\to aa$ by
counting decays, for the Milky Way halo and for the expanding
universe, fixes the parent-share convention, and checks both parts
against `[DMR21]` and `[Yam20]`. Keys refer to [[../references]].

## Result

Parent mass $m_\chi$, line energy $E_0 = m_\chi/2$, lifetime $\tau$,
and $f$ the parent's share of the dark matter **today** times the
branching ratio to $aa$. Both intensities are per steradian.

Milky Way, a line at $E_0$:

$$
I_{\rm line}(\hat n) = \frac{f\,D(\hat n)}{2\pi\,m_\chi\,\tau},
\qquad D(\hat n) = \int\rho_{\rm DM}\,ds ,
$$

with Doppler width $\sigma_E/E_0 = \sigma_v/c = 5.5\times10^{-4}$.

Extragalactic, a continuum below $E_0$:

$$
\frac{dI}{dE} = \frac{c}{4\pi}\;
\frac{2 f\,\rho_{{\rm DM},0}}{m_\chi\,\tau}\;
\frac{e^{\,[t_U - t(z)]/\tau}}{E\,H(z)}\;\Theta(E_0 - E),
\qquad 1 + z = \frac{E_0}{E}.
$$

Code: `source.line_intensity`, `source.line_sigma_kev`,
`source.continuum_intensity` (astropy `Planck18` for $H$, $t$,
$\rho_{{\rm DM},0}$), `source.sky_column` for the full-sky $D$.

## 1. Counting

A parent at rest decays at rate $1/\tau$ into two ALPs, each of energy
$E_0$ when $m_a \ll m_\chi$, so per decay $dN/dE' = 2\,\delta(E' - E_0)$.

**Milky Way.** Parents along a line of sight have number column
$f D(\hat n)/m_\chi$, and each decays now, so the ALP intensity is
$(2/4\pi)\,(f D/m_\chi)(1/\tau)\,\delta(E - E_0)$; integrating over
$E$ gives the line above (`[DMR21]` eq 9–10). Parent velocities
$\sigma_v = 165$ km s⁻¹ (`[EOM19]`, $v_0/\sqrt2$) and the Sun's motion
Doppler-shift the line by $v/c \sim 10^{-3}$; at 7 keV the width is
2 eV, far inside the 170 eV detector resolution
([[../00-baseline/skipper-ccd]]), so the line is a delta at the
detector.

**Extragalactic.** Decays at cosmic time $t$ (scale factor $a$,
$a_0 = 1$) from a parent number density $n_\chi(t)$ emit ALPs at $E'$
that arrive at $E = aE'$ and are diluted by $a^3$. Per unit $E$ today,
with the Jacobian $dE'/dE = 1/a$ (`[DMR21]` eq 5):

$$
\frac{dn_a}{dE} = \int_0^{t_U} dt\; a^3\,\frac{n_\chi(t)}{\tau}\,
\frac{1}{a}\,\frac{dN}{dE'}\Big|_{E' = E/a} .
$$

Parents that have not decayed number $n_\chi(t) = n_\chi^{\rm prim}
a^{-3} e^{-t/\tau}$, where $n_\chi^{\rm prim}$ is the comoving density
had none decayed. With $dt = da/(aH)$ and the delta function fixing
$a_* = E/E_0$:

$$
\frac{dn_a}{dE} = \frac{2\,n_\chi^{\rm prim}}{\tau}\,
\frac{e^{-t(a_*)/\tau}}{E\,H(a_*)}\,\Theta(E_0 - E).
$$

Isotropic relativistic particles give intensity $c\,n/4\pi$ per
steradian, which is the result above once the share is written in
today's terms (§2).

## 2. Which share

The halo column measures parents alive today:
$f\,\rho_{{\rm DM},0} = m_\chi n_\chi^{\rm prim}\,e^{-t_U/\tau}$. So
$n_\chi^{\rm prim} = f\rho_{{\rm DM},0}\,e^{t_U/\tau}/m_\chi$ and the
extragalactic factor becomes $e^{[t_U - t(z)]/\tau} \ge 1$: more
parents were alive when the light we now see was emitted. Writing the
same $f$ in both components makes their ratio independent of the
convention, which is what the joint fit needs. A derivation that puts
$f$ on the primordial density instead multiplies the line by
$e^{-t_U/\tau}$; the two agree only for $\tau \gg t_U$.

## 3. Inputs

| Input | Value | Tag |
|---|---|---|
| Halo | NFW, $r_s = 20$ kpc, $\rho_\odot = 0.4$ GeV cm⁻³, $R_\odot = 8.1$ kpc, cored inside 0.1 kpc (`source.halo`) | `EXT` / `ASSUME` |
| Cosmology | astropy `Planck18` `[Pl18]`: $H_0 = 67.66$, $\Omega_m = 0.311$, $\rho_{{\rm DM},0} = 1.257$ keV cm⁻³, $t_U = 13.79$ Gyr | `EXT` |
| $\int_0^1 da/H(a)$ | 7.64 Gyr $= 0.554\,t_U$ | `DERIV` |
| Halo dispersion | 165 km s⁻¹ | `EXT` |
| Parent | $m_\chi = 7$ keV working case; 2–20 keV keeps $E_0$ in band | `ASSUME` |

## 4. Checks

| # | Check | Test | Result |
|---|---|---|---|
| 1 | Full-sky $\int D\,d\Omega$ against `[DMR21]` fn 8, $2.7\times10^{32}$ eV cm⁻² sr | `test_full_sky_column_matches_dmr` | $2.67\times10^{23}$ GeV cm⁻² sr, 1 % |
| 2 | $\rho_{{\rm DM},0}$ from `Planck18` | `test_dm_density` | 1.257 keV cm⁻³ (`[Yam20]` uses 1.25) |
| 3 | Line units by hand with astropy | `test_line_units_by_hand` | $5.26\times10^9$ cm⁻² s⁻¹ sr⁻¹ at $D = 10^{23}$, 7 keV, $\tau = t_U$ |
| 4 | Line width $\ll$ resolution | `test_line_is_narrow_before_the_detector` | $\sigma_E/E_0 = 5.5\times10^{-4}$ |
| 5 | Continuum support $0 < E < E_0$ | `test_continuum_support` | yes |
| 6 | Continuum shape $E^{1/2} f(m_\chi/2E)$ with $f = (\Omega_m + \Omega_k/x + \Omega_\Lambda/x^3)^{-1/2}$ and coefficient $\tfrac{c}{4\pi}\tfrac{2^{5/2}\rho_{{\rm DM},0}}{H_0 m_\chi^{5/2}\tau}$ | `test_continuum_is_the_yamamoto_power_law` | $3\times10^{-3}$ over $0.2E_0$–$E_0$ |
| 7 | Energy densities at $\tau \gg t_U$: $\rho_{\rm MW}/\rho_{\rm EG}$ and the lifetime at which their sum equals the CMB | `test_energy_densities_match_dmr` | 2.3 (`[DMR21]`: "≈ 2"); $9\times10^3\,t_U$ (`[DMR21]`: "$\lesssim 10^4\,t_U$") |
| 8 | Today's share: intensity per $1/\tau$ rises once $\tau \sim t_U$ | `test_todays_share_against_primordial` | yes |

In `tests/test_source.py`. Check 6 is derived, not fitted: at
$\tau \gg t_U$, $H(a) = H_0 x^{3/2}/f(x)$ with $x = 1/a$ turns the
result into $\tfrac{c}{4\pi}\tfrac{2^{5/2} f\rho_{{\rm DM},0}}
{H_0 m_\chi^{5/2}\tau}\,E^{1/2} f(x)$, the "photon index $+1/2$" of
`[Yam20]`.

## 5. Against `[Yam20]`

| `[Yam20]` | Ours | Agree |
|---|---|---|
| eq 2.2, $I = S\Gamma_{2a}/2\pi m$ | $S \to D$, $\Gamma_{2a} \to f/\tau$ | yes |
| eq 2.5, continuum $\propto E^{1/2} f$ with $2c\Gamma\rho_0/H_0$ | same shape; our coefficient carries $1/4\pi$ per steradian and $e^{[t_U - t]/\tau}$ | yes at $\tau \gg t_U$; theirs has no decay history |
| eq 2.6, $f(x)$ printed with $-\Omega_\Lambda/x^3$ | $+\Omega_\Lambda/x^3$ from Friedmann; with the minus sign $f(1)$ is imaginary | printed sign is a typo; ours stands |
| $\rho_0 = 1.25$ keV cm⁻³, $H_0 = 67.8$ | 1.257, 67.66 | 1 % |

**D28.** The ceiling (`conops.ipynb` figure 6) computes the line with
this note's formula, but scales the continuum from `[Yam20]`'s
*upper limit* on ALP flux ($1.6\times10^{-9}$ erg s⁻¹ cm⁻² sr⁻¹ at
$K = 10^4$ T² m²) by $(g/g_Y)^2\,\Gamma\tau_Y/K_Y$. In the 2–6 keV band
that scaling gives $6.4\times10^{-14}$ photons cm⁻² s⁻¹ sr⁻¹ per
T² m² for the D28 benchmark; the derived spectrum gives
$3.1\times10^{-14}$. D28's continuum count of $1.2\times10^{-3}$ is
therefore $2.1\times$ too high, its line count stands, and the
conclusion (two orders below one count) is unchanged. Figure 6 uses
`source.continuum_intensity` since 2026-09-24: continuum
$5.9\times10^{-4}$ counts ([[../2026-09-24-ceiling-refresh]]).

## Close

Both source components follow from one count with one $f$ and one
$\tau$, agree with `[DMR21]` in the full-sky column (1 %), the energy
ratio, and the CMB-crossing lifetime, and reduce to `[Yam20]`'s
formulae at $\tau \gg t_U$ with the sign in their $f(x)$ corrected.
The unresolved items are inputs, not derivation: the halo core radius
on the exact Centre ray (ALP-CH-16) and the parent mass, which is a
scan variable.

## Links

- contract §1: [[detection-channel-derivation-contract]]
- sources: [[derivation-sources]]
- halo column over the aperture: [[../2026-09-23-source-models]]
- next: Block C, detector counts
