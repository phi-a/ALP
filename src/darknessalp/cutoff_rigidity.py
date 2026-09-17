from math import cos, radians

from darknessalp.constants import R_EARTH_KM


def cutoff_rigidity(mag_lat_deg, r_km):
    """Return the Stormer vertical cut-off rigidity in GV."""
    return 14.9 * cos(radians(mag_lat_deg)) ** 4 / (r_km / R_EARTH_KM) ** 2
