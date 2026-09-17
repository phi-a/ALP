"""Line-of-sight transverse field integral, vectorised over rays."""
import numpy as np
from scipy.integrate import cumulative_trapezoid

from darknessalp.constants import R_EARTH_KM
from darknessalp.field.igrf import igrf_field_eci


def path_end_km(r_eci, n_hats, l_max_re=10.0):
    """Return (s_end, occulted) per ray: Earth surface or the outer sphere."""
    n = np.atleast_2d(n_hats)
    along = n @ r_eci
    r2 = r_eci @ r_eci
    disc = along**2 - r2 + R_EARTH_KM**2
    occulted = (along < 0) & (disc >= 0)
    s_earth = -along - np.sqrt(np.where(occulted, disc, 0.0))
    s_outer = -along + np.sqrt(along**2 - r2 + (l_max_re * R_EARTH_KM) ** 2)
    return np.where(occulted, s_earth, s_outer), occulted


def los_field_integral(r_eci, n_hats, time, coeffs, lmax=13, q_per_m=0.0,
                       l_max_re=10.0, n_steps=200):
    """Return |A| in T m per ray, with running totals and occultation."""
    n = np.atleast_2d(n_hats)
    s_end, occulted = path_end_km(r_eci, n, l_max_re)
    frac = np.linspace(0.0, 1.0, n_steps + 1)
    s_km = s_end[:, None] * frac[None, :]                      # (R, S)
    points = r_eci + s_km[:, :, None] * n[:, None, :]          # (R, S, 3)

    b = igrf_field_eci(points.reshape(-1, 3), time, coeffs, lmax)
    b = b.reshape(points.shape)
    b_along = np.sum(b * n[:, None, :], axis=2, keepdims=True)
    transverse = b - b_along * n[:, None, :]
    phase = np.exp(1j * q_per_m * s_km * 1e3)[:, :, None]

    s_m = np.broadcast_to(s_km[:, :, None] * 1e3, transverse.shape)
    running = cumulative_trapezoid(transverse * phase, s_m, axis=1,
                                   initial=0.0)
    running_tm = np.linalg.norm(running, axis=2)
    return {"amplitude_tm": running_tm[:, -1], "running_tm": running_tm,
            "s_km": s_km, "occulted": occulted}
