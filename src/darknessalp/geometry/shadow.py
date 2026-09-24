"""Conical Earth shadow: sunlit, penumbra, umbra."""
import numpy as np

from darknessalp.constants import R_EQUATOR_KM, R_SUN_KM


def shadow(r_eci, sun_km):
    """Return {lit_fraction, sunlit, penumbra, umbra} arrays per row."""
    r = np.atleast_2d(r_eci)
    to_sun = np.atleast_2d(sun_km) - r
    d_sun = np.linalg.norm(to_sun, axis=1)
    d_earth = np.linalg.norm(r, axis=1)
    a = np.arcsin(R_SUN_KM / d_sun)             # apparent Sun radius
    b = np.arcsin(R_EQUATOR_KM / d_earth)       # apparent Earth radius
    cos_c = -np.sum(r * to_sun, axis=1) / (d_earth * d_sun)
    c = np.maximum(np.arccos(np.clip(cos_c, -1, 1)), 1e-12)

    # Sun disk area behind the Earth disk; b > a in any Earth orbit
    x = (c**2 + a**2 - b**2) / (2 * c)
    y = np.sqrt(np.clip(a**2 - x**2, 0, None))
    hidden = (a**2 * np.arccos(np.clip(x / a, -1, 1))
              + b**2 * np.arccos(np.clip((c - x) / b, -1, 1)) - c * y)
    lit = 1 - hidden / (np.pi * a**2)
    lit = np.where(c >= a + b, 1.0, np.where(c <= b - a, 0.0, lit))
    return {"lit_fraction": lit, "sunlit": lit == 1.0,
            "penumbra": (lit > 0) & (lit < 1), "umbra": lit == 0.0}
