"""Slew angles and times between pointings."""
import numpy as np


def angle_between(u, v):
    """Return degrees between unit vectors, broadcast over rows."""
    dot = np.clip(np.sum(np.atleast_2d(u) * np.atleast_2d(v), axis=1), -1, 1)
    return np.degrees(np.arccos(dot))


def slew_time_s(angle_deg, rate_deg_s=1.5, settle_s=60.0):
    """Return time to slew at a fixed rate plus settle (ASSUME 1.5 deg/s)."""
    return np.asarray(angle_deg) / rate_deg_s + settle_s
