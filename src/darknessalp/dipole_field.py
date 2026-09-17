from darknessalp.constants import R_EARTH_KM


def dipole_field(r_ecef_km, coeffs):
    """Return the tilted centred dipole field in tesla, Earth-fixed axes."""
    x, y, z = r_ecef_km
    r2 = x * x + y * y + z * z
    gx, gy = coeffs[(1, 1)]
    gz = coeffs[(1, 0)][0]

    # B = (a/r)^3 [3 (G . r_hat) r_hat - G]
    dot = (gx * x + gy * y + gz * z) / r2
    scale = (R_EARTH_KM**2 / r2) ** 1.5 * 1e-9
    return (scale * (3 * dot * x - gx),
            scale * (3 * dot * y - gy),
            scale * (3 * dot * z - gz))
