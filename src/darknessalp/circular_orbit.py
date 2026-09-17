from math import cos, radians, sin, sqrt

from darknessalp.constants import (
    J2, MU_EARTH_KM3_S2, R_EARTH_KM, R_EQUATOR_KM)


def circular_orbit(t_s, alt_km, inc_deg, raan_deg=0.0, u0_deg=0.0):
    """Return ECI position (km) and velocity (km/s) at t_s after epoch."""
    a = R_EARTH_KM + alt_km
    n = sqrt(MU_EARTH_KM3_S2 / a**3)
    i = radians(inc_deg)

    # J2 nodal regression: the one perturbation that matters here
    raan_dot = -1.5 * n * J2 * (R_EQUATOR_KM / a) ** 2 * cos(i)
    raan = radians(raan_deg) + raan_dot * t_s
    u = radians(u0_deg) + n * t_s

    cu, su = cos(u), sin(u)
    cw, sw = cos(raan), sin(raan)
    ci, si = cos(i), sin(i)
    r = (a * (cu * cw - su * sw * ci),
         a * (cu * sw + su * cw * ci),
         a * su * si)
    v = (a * n * (-su * cw - cu * sw * ci),
         a * n * (-su * sw + cu * cw * ci),
         a * n * cu * si)
    return r, v
