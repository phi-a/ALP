"""GCRF <-> EME2000 (J2000 mean equator and equinox): the frame bias."""
import numpy as np
from astropy import units as u
from astropy.coordinates import GCRS, PrecessedGeocentric
from astropy.time import Time

from darknessalp.frames.eci_ecef import _xyz

_J2000 = Time("J2000")
# columns: the GCRF axes seen on EME2000 axes (IERS bias, 23 mas)
BIAS = GCRS(_xyz(np.eye(3)), obstime=_J2000).transform_to(
    PrecessedGeocentric(equinox="J2000", obstime=_J2000)
).cartesian.xyz.to_value(u.km)


def gcrf_to_eme2000(v):
    """Return (N, 3) vectors on EME2000 axes for (N, 3) GCRF vectors."""
    return np.atleast_2d(v) @ BIAS.T


def eme2000_to_gcrf(v):
    """Return (N, 3) vectors on GCRF axes for (N, 3) EME2000 vectors."""
    return np.atleast_2d(v) @ BIAS
