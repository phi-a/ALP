---
type: reference
tags: [darkness, alp, tooling, api]
created: 2026-09-17
updated: 2026-09-17
status: active
---

# API reference

Every public function in `src/darknessalp/`, with its
signature and docstring. **Generated** — do not edit by hand:

```powershell
python scripts/api_reference.py Notebook/02-mission-analysis/api-reference.md
```

Conventions: positions in km, fields in tesla, angles in
degrees, time as an astropy `Time`. Arrays are `(N, 3)` for
vectors and `(N,)` for scalars; a single row is accepted
wherever `(N, 3)` is.

## `background`

Celestial and particle background models.

| Call | Returns |
|---|---|
| `SOURCES` | constant: 18 entries |
| `cxb_intensity(e_kev)` | Return photons cm^-2 s^-1 sr^-1 keV^-1 at energy e_kev. |
| `cxb_rate(area_cm2, omega_sr, e_lo=1.0, e_hi=10.0)` | Return counts s^-1 in a band for a given grasp. |
| `grxe_brightness(l_deg, b_deg)` | Return 2-10 keV surface brightness at Galactic (l, b). |
| `nxb_proxy(cutoff_gv, index=1.0, reference_gv=10.0)` | Return a relative NXB level, 1 at reference_gv, scaling Rc^-index. |
| `source_vectors()` | Return (names, (N, 3) unit vectors, mCrab array). |
| `sources_in_cone(n_hat, half_angle_deg=10.0)` | Return [(name, separation_deg, mCrab)] inside the cone. |

## `detector`

The skipper-CCD response: efficiency, resolution, counts.

| Call | Returns |
|---|---|
| `expected_counts(e_kev, intensity, e_edges_kev, prob, dt_s, qe=None, area_cm2=12.0, half_angle_deg=10.0, live=0.5, select=1.0, fwhm_kev=None)` | Return counts (samples, bins) for an ALP intensity per keV per sr. |
| `grasp_cm2sr(area_cm2=12.0, half_angle_deg=10.0)` | Return geometric area times the cone solid angle. |
| `quantum_efficiency(e_kev, al_nm=50.0, thickness_um=500.0, dead_um=0.0)` | Return window transmission times silicon absorption. |
| `redistribution(e_kev, e_edges_kev, fwhm_kev=None)` | Return R[E, j]: the fraction of events at E measured in bin j. |
| `resolution_fwhm_kev(e_kev, noise_fwhm_kev=0.119, fano=0.118, w_ev=3.72)` | Return FWHM in keV: Fano broadening and readout noise in quadrature. |
| `silicon_absorption(e_kev, thickness_um=500.0, dead_um=0.0)` | Return the fraction absorbed in the active silicon. |
| `window_transmission(e_kev, al_nm=50.0)` | Return the fraction passing an aluminium entrance window. |

## `dynamics`

Accelerations and torques. Models only, no integration.

| Call | Returns |
|---|---|
| `j2_acceleration(r)` | Return the J2 oblateness acceleration. |
| `two_body(r)` | Return the point-mass acceleration. |
| `two_body_j2(r)` | Return two-body plus J2 acceleration. |

## `field`

The geomagnetic field and magnetic coordinates.

| Call | Returns |
|---|---|
| `cutoff_rigidity(mag_lat_deg, r_km)` | Return the Stormer vertical cut-off rigidity in GV. |
| `dipole_axis(coeffs)` | Return the unit vector of the dipole axis toward magnetic north. |
| `dipole_field(r_ecef, coeffs)` | Return the dipole field in tesla, ECEF axes, for (N, 3) points. |
| `dipole_moment(coeffs)` | Return the degree-1 coefficient vector (g11, h11, g10) in nT. |
| `igrf_field(r_ecef, coeffs, lmax=13)` | Return the field in tesla, ECEF axes, for (N, 3) ECEF points in km. |
| `igrf_field_eci(r_eci, time, coeffs, lmax=13)` | Return the field in tesla, ECI axes, for (N, 3) ECI points. |
| `l_shell(mag_lat_deg, r_km)` | Return the dipole L-shell of a point. |
| `load_igrf(year, path='data/bfield/igrf14coeffs.txt')` | Return (g, h) arrays [n, m] in nT at a decimal year. |
| `magnetic_latitude(r_ecef, coeffs)` | Return dipole magnetic latitude in degrees for (N, 3) ECEF points. |
| `schmidt_legendre(nmax, theta)` | Return P[n][m] and dP/dtheta[n][m], each shaped like theta. |

## `frames`

Time and reference frames. astropy does the work.

| Call | Returns |
|---|---|
| `decimal_year(time)` | Return the decimal year of a Time (scalar or array). |
| `ecef_to_eci(v_ecef, time)` | Return (N, 3) ECI vectors for (N, 3) ECEF vectors at Time(s). |
| `eci_to_ecef(v_eci, time)` | Return (N, 3) ECEF vectors for (N, 3) ECI vectors at Time(s). |
| `eme2000_to_gcrf(v)` | Return (N, 3) vectors on GCRF axes for (N, 3) EME2000 vectors. |
| `galactic_vector(l_deg, b_deg)` | Return unit vectors toward Galactic (l, b) in degrees. |
| `gcrf_to_eme2000(v)` | Return (N, 3) vectors on EME2000 axes for (N, 3) GCRF vectors. |
| `radec_vector(ra_deg, dec_deg)` | Return unit vectors toward J2000 (ra, dec) in degrees. |
| `spherical(r_ecef)` | Return geocentric (lat_deg, lon_deg, r_km) arrays of ECEF points. |
| `sun_vector(time)` | Return (N, 3) unit vectors toward the Sun at Time(s). |
| `times(epoch, t_s)` | Return Time for seconds after an ISO, Julian-date or Time epoch. |
| `to_galactic(v)` | Return Galactic (l_deg, b_deg) of (N, 3) ICRS unit vectors. |
| `unit_vector(coord)` | Return (N, 3) ICRS unit vectors of a SkyCoord (ICRS ~ GCRS here). |

## `geometry`

Lines of sight, the Earth disk, and the field of view.

| Call | Returns |
|---|---|
| `cone_directions(n_hat, half_angle_deg=10.0, rings=3)` | Return (M, 3) directions and equal-area weights sampling the cone. |
| `conversion_probability(amplitude_tm, g_gev)` | Return P(a -> gamma) = (g |A| / 2)^2 for |A| in T m, g in GeV^-1. |
| `earth_angular_radius_deg(r_eci)` | Return the angular radius of the Earth disk from the spacecraft. |
| `fov_axes(n_hat, up_hint=(0.0, 0.0, 1.0))` | Return (x_hat, y_hat) across the boresight; y_hat toward up_hint. |
| `fov_field_integral(r_eci, n_hat, time, coeffs, lmax=13, q_per_m=0.0, half_angle_deg=10.0, rings=3)` | Return FOV-mean |A|^2 in T^2 m^2, per-ray |A|; ray 0 = boresight. |
| `in_umbra(r_eci, sun_hats)` | Return a bool per row: spacecraft inside the cylindrical shadow. |
| `limb_angle(r_eci, n_hats)` | Return degrees from boresight(s) to the limb; negative = at Earth. |
| `limb_directions(r_eci, n_points=180)` | Return (n_points, 3) unit vectors along the limb ring. |
| `los_field_integral(r_eci, n_hats, time, coeffs, lmax=13, q_per_m=0.0, l_max_re=10.0, n_steps=200, end_alt_km=150.0)` | Return |A| in T m per ray, with running totals and occultation. |
| `offset_direction(x_deg, y_deg, n_hat, x_hat, y_hat)` | Return unit vectors at angular offsets (x, y) from the boresight. |
| `path_end_km(r_eci, n_hats, l_max_re=10.0, end_alt_km=150.0)` | Return (s_end, occulted): the opaque-air shell or the outer sphere. |
| `project(v, n_hat, x_hat, y_hat)` | Return (x_deg, y_deg) offsets; radius is the true angle from centre. |
| `transverse_amplitude(b, n_hats, s_m, q_per_m=0.0)` | Return running |int B_perp e^{iqs} ds| in T m, shape (R, S). |

## `kinematics`

Body attitude, slews, and rate-limited steering.

| Call | Returns |
|---|---|
| `angle_between(u, v)` | Return degrees between unit vectors, broadcast over rows. |
| `boresight(rotation)` | Return (N, 3) ECI boresight(s) of body->ECI Rotation(s). |
| `look_at(boresight_eci, hint=(0.0, 0.0, 1.0))` | Return body->ECI Rotation(s): +Z on the boresight, +Y toward hint. |
| `radiator_normal(rotation)` | Return (N, 3) ECI radiator normal(s) of body->ECI Rotation(s). |
| `slew_time_s(angle_deg, rate_deg_s=1.5, settle_s=60.0)` | Return time to slew at a fixed rate plus settle (ASSUME 1.5 deg/s). |
| `steer(desired, t_s, rate_deg_s=1.5, settle_deg=0.1, start=None, mode_index=None)` | Return (commanded Rotations, error_deg, slewing) at a fixed rate. |

## `likelihood`

Fisher information and fits for the linear count model.

| Call | Returns |
|---|---|
| `fisher(templates, mu)` | Return I_ab = sum over cells of t_a t_b / mu. |
| `fit_amplitudes(counts, templates, mu)` | Return least-squares amplitudes with weights 1/mu. |
| `information_fraction(signal, nuisance, mu)` | Return the share of the signal's information that survives profiling. |
| `profiled_sigma(signal, nuisance, mu)` | Return the error on the signal amplitude after profiling nuisance. |
| `upper_limit(sigma, cl=0.9)` | Return the one-sided Gaussian upper limit on a null amplitude. |

## `orbit`

Where the spacecraft is.

| Call | Returns |
|---|---|
| `elements_to_state(a_km, e, inc_deg, raan_deg, argp_deg, nu_deg, mu=398600.4418)` | Return position (N, 3) km and velocity (N, 3) km/s from elements. |
| `period_s(a_km, mu=398600.4418)` | Return the two-body orbital period in seconds. |
| `propagate(r0, v0, t_s, gravity='j2')` | Return r (N, 3) km and v (N, 3) km/s at t_s >= 0 s after the epoch. |
| `read_oem(path)` | Return (Time, r (N, 3) km, v (N, 3) km/s) on GCRF axes from an OEM. |
| `write_oem(path, time, r, v, ref_frame='GCRF', object_name='DARKNESS')` | Write GCRF states (km, km/s) as a CCSDS OEM on ref_frame axes. |

## `pointing`

What to look at, and when.

| Call | Returns |
|---|---|
| `BODIES` | constant: 7 entries |
| `GALACTIC` | constant: {apex, gc} |
| `attitudes(modes, mode_index, time, r_eci, v_eci, b_eci=None)` | Return Rotation(s) following mode_index (N,) into a list of modes. |
| `body_direction(name, time, r_eci)` | Return (N, 3) directions to a solar-system body from the spacecraft. |
| `conditions(time, r_eci, extra=None)` | Return {name: bool (N,)} with umbra, sunlit, always, plus extra. |
| `desired_attitude(m, time, r_eci, v_eci, b_eci=None)` | Return body->ECI Rotation(s) realising a mode at each sample. |
| `feasible(r_eci, n_hats, sun_hat, sun_min=90.0, limb_min=0.0)` | Return a bool per boresight: outside the Sun and limb keep-outs. |
| `mode(primary, roll='anti_earth')` | Return a mode dict; roll: anti_earth, anti_sun, or a target spec. |
| `select(rules, conds)` | Return (mode_index (N,), modes) for [(condition, mode), ...]. |
| `sky_target(name)` | Return one unit vector for a named sky target or 'ra,dec'. |
| `sun_angle(n_hats, sun_hats)` | Return degrees between boresight(s) and the Sun. |
| `target_direction(spec, time, r_eci, v_eci=None, b_eci=None)` | Return (N, 3) boresight targets for a spec string. |

## `sim`

The per-sample record every run produces.

| Call | Returns |
|---|---|
| `state_table(epoch, t_s, r_eci, boresights, lmax=13, q_per_m=0.0, half_angle_deg=10.0)` | Return a dict of arrays, one entry per sample, for a pointing law. |
| `to_csv(table, path)` | Write a state table to CSV with a header row. |

## `source`

Where the ALPs come from: the dark-matter halo column.

| Call | Returns |
|---|---|
| `column_density(l_deg, b_deg, r_max_kpc=200.0, **nfw)` | Return D = int rho ds in GeV cm^-2 toward Galactic (l, b), per row. |
| `continuum_intensity(e_kev, m_kev, share, tau_gyr, cosmo=FlatLambdaCDM(name='Planck18', H0=<Quantity 67.66 km / (Mpc s)>, Om0=0.30966, Tcmb0=<Quantity 2.7255 K>, Neff=3.046, m_nu=<Quantity [0.  , 0.  , 0.06] eV>, Ob0=0.04897))` | Return the redshifted chi -> aa intensity, cm^-2 s^-1 sr^-1 keV^-1. |
| `dm_density_kev_cm3(cosmo=FlatLambdaCDM(name='Planck18', H0=<Quantity 67.66 km / (Mpc s)>, Om0=0.30966, Tcmb0=<Quantity 2.7255 K>, Neff=3.046, m_nu=<Quantity [0.  , 0.  , 0.06] eV>, Ob0=0.04897))` | Return today's mean dark-matter density in keV cm^-3. |
| `line_intensity(d_gevcm2, m_kev, share, tau_gyr)` | Return the Milky Way chi -> aa line intensity, cm^-2 s^-1 sr^-1. |
| `line_sigma_kev(m_kev, sigma_v_kms=165.0)` | Return the halo Doppler width (one sigma) of the line at m/2, keV. |
| `nfw_density(r_kpc, rho_s=0.31979205000000005, r_s_kpc=20.0, r_core_kpc=0.1)` | Return the NFW density in GeV cm^-3 at Galactocentric radius r_kpc. |
| `sky_column(step_deg=2.0, **nfw)` | Return the full-sky integral of D in GeV cm^-2 sr on an (l, b) grid. |

## Links

- part of [[../ALP]]
- why these exist: [[tooling]], [[pointing-system]]
- the pipeline: `jupyter/main_sequence.ipynb`
