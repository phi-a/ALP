"""Cosmic X-ray background, De Luca & Molendi 2004 power law."""
import numpy as np


def cxb_intensity(e_kev):
    """Return photons cm^-2 s^-1 sr^-1 keV^-1 at energy e_kev."""
    return 11.6 * np.asarray(e_kev, float) ** -1.41


def cxb_rate(area_cm2, omega_sr, e_lo=1.0, e_hi=10.0):
    """Return counts s^-1 in a band for a given grasp."""
    integral = 11.6 * (e_hi**-0.41 - e_lo**-0.41) / -0.41
    return integral * area_cm2 * omega_sr
