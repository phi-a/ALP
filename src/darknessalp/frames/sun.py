"""Sun direction in GCRS, via astropy."""
import numpy as np
from astropy.coordinates import get_sun


def sun_vector(time):
    """Return (N, 3) unit vectors toward the Sun at Time(s)."""
    xyz = np.atleast_2d(get_sun(time).cartesian.xyz.value.T)
    return xyz / np.linalg.norm(xyz, axis=1, keepdims=True)
