"""GCRS (ECI) <-> ITRS (ECEF) for positions and vectors, via astropy."""
import numpy as np
from astropy import units as u
from astropy.coordinates import GCRS, ITRS, CartesianRepresentation


def _xyz(v):
    v = np.atleast_2d(v)
    return CartesianRepresentation(v[:, 0], v[:, 1], v[:, 2], unit=u.km)


def eci_to_ecef(v_eci, time):
    """Return (N, 3) ECEF vectors for (N, 3) ECI vectors at Time(s)."""
    out = GCRS(_xyz(v_eci), obstime=time).transform_to(ITRS(obstime=time))
    return out.cartesian.xyz.to_value(u.km).T


def ecef_to_eci(v_ecef, time):
    """Return (N, 3) ECI vectors for (N, 3) ECEF vectors at Time(s)."""
    out = ITRS(_xyz(v_ecef), obstime=time).transform_to(GCRS(obstime=time))
    return out.cartesian.xyz.to_value(u.km).T


def spherical(r_ecef):
    """Return geocentric (lat_deg, lon_deg, r_km) arrays of ECEF points."""
    r_ecef = np.atleast_2d(r_ecef)
    rho = np.hypot(r_ecef[:, 0], r_ecef[:, 1])
    lat = np.degrees(np.arctan2(r_ecef[:, 2], rho))
    lon = np.degrees(np.arctan2(r_ecef[:, 1], r_ecef[:, 0]))
    return lat, lon, np.hypot(rho, r_ecef[:, 2])
