"""Analytic circular orbit with secular J2 node regression."""
import numpy as np

from darknessalp.constants import (
    J2, MU_EARTH_KM3_S2, R_EARTH_KM, R_EQUATOR_KM)


def circular_orbit(t_s, alt_km, inc_deg, raan_deg=0.0, u0_deg=0.0):
    """Return ECI position (N, 3) km and velocity (N, 3) km/s."""
    t = np.atleast_1d(t_s).astype(float)
    a = R_EARTH_KM + alt_km
    n = np.sqrt(MU_EARTH_KM3_S2 / a**3)
    i = np.radians(inc_deg)

    # secular J2 rates of the node and of the argument of latitude
    k = 1.5 * n * J2 * (R_EQUATOR_KM / a) ** 2
    raan_dot = -k * np.cos(i)
    u_dot = n + k * (3 - 4 * np.sin(i) ** 2)
    w = np.radians(raan_deg) + raan_dot * t
    u = np.radians(u0_deg) + u_dot * t

    cu, su, cw, sw = np.cos(u), np.sin(u), np.cos(w), np.sin(w)
    ci, si = np.cos(i), np.sin(i)
    r = a * np.stack([cu * cw - su * sw * ci,
                      cu * sw + su * cw * ci,
                      su * si], axis=1)
    v = a * n * np.stack([-su * cw - cu * sw * ci,
                          -su * sw + cu * cw * ci,
                          cu * si], axis=1)
    return r, v


def period_s(alt_km):
    """Return the circular orbital period in seconds."""
    return 2 * np.pi * np.sqrt((R_EARTH_KM + alt_km) ** 3 / MU_EARTH_KM3_S2)
