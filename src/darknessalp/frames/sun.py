"""Sun position and direction in GCRS, via astropy."""
import numpy as np
from astropy.coordinates import get_sun


def sun_position(time):
    """Return (N, 3) geocentric Sun positions in km at Time(s)."""
    return np.atleast_2d(get_sun(time).cartesian.xyz.to_value("km").T)


def sun_vector(time):
    """Return (N, 3) unit vectors toward the Sun at Time(s)."""
    xyz = sun_position(time)
    return xyz / np.linalg.norm(xyz, axis=1, keepdims=True)
