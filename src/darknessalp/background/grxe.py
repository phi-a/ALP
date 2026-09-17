"""Galactic ridge X-ray emission, two-component analytic (ASSUME)."""
import numpy as np

# 2-10 keV surface brightness, erg s^-1 cm^-2 deg^-2; scale angles in deg.
# Bulge and disk terms shaped after Revnivtsev et al. 2006; normalised so
# the inner ridge (l ~ 20, b = 0) is ~8.6e-11. Replace with a NIR-traced
# model before quoting a number.
BULGE_PEAK, BULGE_L, BULGE_B = 3.0e-10, 8.0, 4.0
DISK_PEAK, DISK_L, DISK_B = 1.0e-10, 60.0, 1.7


def grxe_brightness(l_deg, b_deg):
    """Return 2-10 keV surface brightness at Galactic (l, b)."""
    l = (np.asarray(l_deg, float) + 180) % 360 - 180
    b = np.asarray(b_deg, float)
    bulge = BULGE_PEAK * np.exp(-np.abs(l) / BULGE_L - np.abs(b) / BULGE_B)
    disk = DISK_PEAK * np.exp(-np.abs(l) / DISK_L - np.abs(b) / DISK_B)
    return bulge + disk
