from darknessalp.constants import R_EARTH_KM


def in_umbra(r_eci_km, sun_hat):
    """Return True inside the cylindrical Earth shadow."""
    x, y, z = r_eci_km
    along = x * sun_hat[0] + y * sun_hat[1] + z * sun_hat[2]
    if along >= 0.0:
        return False

    across2 = x * x + y * y + z * z - along * along
    return across2 < R_EARTH_KM**2
