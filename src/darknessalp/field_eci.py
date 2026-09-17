from darknessalp.ecef_to_eci import ecef_to_eci
from darknessalp.eci_to_ecef import eci_to_ecef
from darknessalp.igrf_field import igrf_field


def field_eci(r_eci_km, gmst_deg, coeffs, lmax=13):
    """Return the IGRF field in tesla, ECI axes, at an ECI point."""
    b_ecef = igrf_field(eci_to_ecef(r_eci_km, gmst_deg), coeffs, lmax)
    return ecef_to_eci(b_ecef, gmst_deg)
