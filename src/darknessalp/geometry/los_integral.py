"""Line-of-sight transverse field integral, vectorised over rays."""
import numpy as np
from scipy.integrate import cumulative_trapezoid

from darknessalp.constants import (
    EV2_PER_TESLA, INV_EV_PER_M, R_EARTH_KM)
from darknessalp.field.igrf import igrf_field_eci
from darknessalp.geometry.fov import cone_directions


def path_end_km(r_eci, n_hats, l_max_re=10.0, end_alt_km=150.0):
    """Return (s_end, occulted): the opaque-air shell or the outer sphere."""
    n = np.atleast_2d(n_hats)
    along = n @ r_eci
    r2 = r_eci @ r_eci
    disc = along**2 - r2 + R_EARTH_KM**2
    occulted = (along < 0) & (disc >= 0)          # hits the ground
    shell = along**2 - r2 + (R_EARTH_KM + end_alt_km) ** 2
    blocked = (along < 0) & (shell >= 0)          # enters opaque air
    s_shell = -along - np.sqrt(np.where(blocked, shell, 0.0))
    s_outer = -along + np.sqrt(along**2 - r2 + (l_max_re * R_EARTH_KM) ** 2)
    return np.where(blocked, s_shell, s_outer), occulted


def los_field_integral(r_eci, n_hats, time, coeffs, lmax=13, q_per_m=0.0,
                       l_max_re=10.0, n_steps=200, end_alt_km=150.0):
    """Return |A| in T m per ray, with running totals and occultation."""
    n = np.atleast_2d(n_hats)
    s_end, occulted = path_end_km(r_eci, n, l_max_re, end_alt_km)
    frac = np.linspace(0.0, 1.0, n_steps + 1)
    s_km = s_end[:, None] * frac[None, :]                      # (R, S)
    points = r_eci + s_km[:, :, None] * n[:, None, :]          # (R, S, 3)

    b = igrf_field_eci(points.reshape(-1, 3), time, coeffs, lmax)
    running_tm = transverse_amplitude(b.reshape(points.shape), n,
                                      s_km * 1e3, q_per_m)
    return {"amplitude_tm": running_tm[:, -1], "running_tm": running_tm,
            "s_km": s_km, "occulted": occulted}


def transverse_amplitude(b, n_hats, s_m, q_per_m=0.0):
    """Return running |int B_perp e^{iqs} ds| in T m, shape (R, S)."""
    n = np.atleast_2d(n_hats)
    b_along = np.sum(b * n[:, None, :], axis=2, keepdims=True)
    transverse = b - b_along * n[:, None, :]
    phase = np.exp(1j * q_per_m * s_m)[:, :, None]

    s = np.broadcast_to(s_m[:, :, None], transverse.shape)
    running = cumulative_trapezoid(transverse * phase, s, axis=1,
                                   initial=0.0)
    return np.linalg.norm(running, axis=2)


def conversion_probability(amplitude_tm, g_gev):
    """Return P(a -> gamma) = (g |A| / 2)^2 for |A| in T m, g in GeV^-1."""
    amp_ev = np.asarray(amplitude_tm) * EV2_PER_TESLA * INV_EV_PER_M
    return (g_gev * 1e-9 * amp_ev / 2) ** 2


def fov_field_integral(r_eci, n_hat, time, coeffs, lmax=13, q_per_m=0.0,
                       half_angle_deg=10.0, rings=3):
    """Return FOV-mean |A|^2 in T^2 m^2, per-ray |A|; ray 0 = boresight."""
    dirs, weights = cone_directions(n_hat, half_angle_deg, rings)
    res = los_field_integral(r_eci, dirs, time, coeffs, lmax=lmax,
                             q_per_m=q_per_m)
    amp = res["amplitude_tm"]
    return {"k_t2m2": float(np.sum(weights * amp**2)),
            "amplitude_tm": amp, "occulted": res["occulted"],
            "weights": weights, "dirs": dirs}
