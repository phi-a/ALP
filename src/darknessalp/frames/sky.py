"""Sky directions as ECI unit vectors, via astropy SkyCoord."""
import numpy as np
from astropy.coordinates import SkyCoord


def unit_vector(coord):
    """Return (N, 3) ICRS unit vectors of a SkyCoord (ICRS ~ GCRS here)."""
    return np.atleast_2d(coord.icrs.cartesian.xyz.value.T)


def radec_vector(ra_deg, dec_deg):
    """Return unit vectors toward J2000 (ra, dec) in degrees."""
    return unit_vector(SkyCoord(ra_deg, dec_deg, unit="deg", frame="icrs"))


def galactic_vector(l_deg, b_deg):
    """Return unit vectors toward Galactic (l, b) in degrees."""
    return unit_vector(SkyCoord(l_deg, b_deg, unit="deg", frame="galactic"))


def to_galactic(v):
    """Return Galactic (l_deg, b_deg) of (N, 3) ICRS unit vectors."""
    v = np.atleast_2d(v)
    c = SkyCoord(x=v[:, 0], y=v[:, 1], z=v[:, 2], frame="icrs",
                 representation_type="cartesian").galactic
    return c.l.deg, c.b.deg
