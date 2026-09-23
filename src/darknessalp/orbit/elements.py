"""Osculating Keplerian elements (the CCSDS OPM set) to a Cartesian state."""
import numpy as np
from scipy.spatial.transform import Rotation

from darknessalp.constants import MU_EARTH_KM3_S2


def elements_to_state(a_km, e, inc_deg, raan_deg, argp_deg, nu_deg,
                      mu=MU_EARTH_KM3_S2):
    """Return position (N, 3) km and velocity (N, 3) km/s from elements."""
    a, e, inc, raan, argp, nu = np.broadcast_arrays(
        *(np.atleast_1d(x).astype(float) for x in (a_km, e, inc_deg,
                                                    raan_deg, argp_deg,
                                                    nu_deg)))
    p = a * (1 - e**2)
    nu = np.radians(nu)
    zero = np.zeros_like(nu)

    # perifocal frame: x to periapsis, z along the orbit normal
    r_pf = (p / (1 + e * np.cos(nu)))[:, None] * np.stack(
        [np.cos(nu), np.sin(nu), zero], axis=1)
    v_pf = np.sqrt(mu / p)[:, None] * np.stack(
        [-np.sin(nu), e + np.cos(nu), zero], axis=1)
    rot = Rotation.from_euler("ZXZ", np.stack([raan, inc, argp], axis=1),
                              degrees=True)
    return rot.apply(r_pf), rot.apply(v_pf)


def period_s(a_km, mu=MU_EARTH_KM3_S2):
    """Return the two-body orbital period in seconds."""
    return 2 * np.pi * np.sqrt(np.asarray(a_km, float) ** 3 / mu)
