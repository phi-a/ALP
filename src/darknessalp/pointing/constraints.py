"""Pointing keep-outs. Angles in degrees; ASSUME values until the ICD."""
import numpy as np

from darknessalp.geometry.limb import limb_angle
from darknessalp.kinematics.slew import angle_between


def sun_angle(n_hats, sun_hats):
    """Return degrees between boresight(s) and the Sun."""
    return angle_between(n_hats, sun_hats)


def feasible(r_eci, n_hats, sun_hat, sun_min=90.0, limb_min=0.0):
    """Return a bool per boresight: outside the Sun and limb keep-outs."""
    n = np.atleast_2d(n_hats)
    ok_sun = sun_angle(n, np.tile(sun_hat, (len(n), 1))) >= sun_min
    return ok_sun & (limb_angle(r_eci, n) >= limb_min)
