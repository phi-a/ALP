"""Target directions per sample, (N, 3) ECI unit vectors, from a spec."""
import numpy as np
from astropy.coordinates import get_body

from darknessalp.frames.sky import galactic_vector, radec_vector
from darknessalp.frames.sun import sun_vector

GALACTIC = {"gc": (0.0, 0.0), "apex": (57.0, 22.0)}  # apex: ASSUME
BODIES = ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")


def _unit(v):
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def sky_target(name):
    """Return one unit vector for a named sky target or 'ra,dec'."""
    if name in GALACTIC:
        return galactic_vector(*GALACTIC[name])[0]
    ra, dec = (float(s) for s in name.split(","))
    return radec_vector(ra, dec)[0]


def body_direction(name, time, r_eci):
    """Return (N, 3) directions to a solar-system body from the spacecraft."""
    pos = get_body(name, time).cartesian.xyz.to_value("km").T
    return _unit(np.atleast_2d(pos) - np.atleast_2d(r_eci))


def target_direction(spec, time, r_eci, v_eci=None, b_eci=None):
    """Return (N, 3) boresight targets for a spec string."""
    r = np.atleast_2d(r_eci)
    n = len(r)
    if spec in BODIES:
        return body_direction(spec, time, r)
    if spec == "anti_sun":
        return -sun_vector(time)
    if spec == "zenith":
        return _unit(r)
    if spec == "nadir":
        return -_unit(r)
    if spec in ("velocity", "anti_velocity"):
        v = _unit(np.atleast_2d(v_eci))
        return v if spec == "velocity" else -v
    if spec in ("orbit_normal", "anti_orbit_normal"):
        h = _unit(np.cross(r, np.atleast_2d(v_eci)))
        return h if spec == "orbit_normal" else -h
    if spec == "b_perp":            # across the field, toward the sky
        return _unit(np.cross(np.cross(b_eci, r), b_eci))
    if spec == "b_along":           # along the field, sky-side half
        b = _unit(np.atleast_2d(b_eci))
        sign = np.sign(np.sum(b * r, axis=1, keepdims=True))
        return b * np.where(sign == 0, 1.0, sign)
    return np.tile(sky_target(spec), (n, 1))
