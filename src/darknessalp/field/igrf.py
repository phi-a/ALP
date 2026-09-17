"""IGRF-14 main field, vectorised over points."""
from pathlib import Path

import numpy as np

from darknessalp.constants import R_EARTH_KM
from darknessalp.frames.eci_ecef import ecef_to_eci, eci_to_ecef

IGRF_PATH = (Path(__file__).resolve().parents[3] / "data" / "bfield"
             / "igrf14coeffs.txt")


def load_igrf(year, path=IGRF_PATH):
    """Return (g, h) arrays [n, m] in nT at a decimal year."""
    rows = [line.split() for line in Path(path).read_text().splitlines()
            if line and not line.startswith("#")]
    epochs = np.array(rows[1][3:-1], float)
    if not epochs[0] <= year <= epochs[-1] + 5:
        raise ValueError("year outside the model range")

    # last column is secular variation for the five years past the end
    k = int(np.searchsorted(epochs, year, side="right") - 1)
    last = k == len(epochs) - 1
    f = year - epochs[k] if last else (year - epochs[k]) / 5.0
    g = np.zeros((14, 14))
    h = np.zeros((14, 14))
    for row in rows[2:]:
        n, m, v = int(row[1]), int(row[2]), np.array(row[3:], float)
        value = v[k] + f * (v[-1] if last else v[k + 1] - v[k])
        (g if row[0] == "g" else h)[n, m] = value
    return g, h


def schmidt_legendre(nmax, theta):
    """Return P[n][m] and dP/dtheta[n][m], each shaped like theta."""
    ct, st = np.cos(theta), np.sin(theta)
    p = np.zeros((nmax + 1, nmax + 1) + theta.shape)
    dp = np.zeros_like(p)
    p[0, 0] = 1.0
    for n in range(1, nmax + 1):
        k = np.sqrt((2 * n - 1) / (2 * n)) if n > 1 else 1.0
        p[n, n] = k * st * p[n - 1, n - 1]
        dp[n, n] = k * (st * dp[n - 1, n - 1] + ct * p[n - 1, n - 1])
        for m in range(n):
            c1 = (2 * n - 1) / np.sqrt(n * n - m * m)
            c2 = np.sqrt((n - 1) ** 2 - m * m) / np.sqrt(n * n - m * m)
            p[n, m] = c1 * ct * p[n - 1, m] - c2 * p[n - 2, m]
            dp[n, m] = (c1 * (ct * dp[n - 1, m] - st * p[n - 1, m])
                        - c2 * dp[n - 2, m])
    return p, dp


def igrf_field(r_ecef, coeffs, lmax=13):
    """Return the field in tesla, ECEF axes, for (N, 3) ECEF points in km."""
    g, h = coeffs
    r_ecef = np.atleast_2d(r_ecef)
    x, y, z = r_ecef.T
    rho = np.hypot(x, y)
    r = np.hypot(rho, z)
    theta, phi = np.arctan2(rho, z), np.arctan2(y, x)
    p, dp = schmidt_legendre(lmax, theta)

    b_r = np.zeros_like(r)
    b_t = np.zeros_like(r)
    b_p = np.zeros_like(r)
    for n in range(1, lmax + 1):
        scale = (R_EARTH_KM / r) ** (n + 2)
        for m in range(n + 1):
            cm, sm = np.cos(m * phi), np.sin(m * phi)
            gh = g[n, m] * cm + h[n, m] * sm
            b_r += (n + 1) * scale * gh * p[n, m]
            b_t -= scale * gh * dp[n, m]
            b_p += scale * m * (g[n, m] * sm - h[n, m] * cm) * p[n, m]

    st = np.sin(theta)
    b_p = np.where(st > 1e-12, b_p / np.where(st > 1e-12, st, 1.0), 0.0)

    # local (r, theta, phi) -> Cartesian
    ct, cp, sp = np.cos(theta), np.cos(phi), np.sin(phi)
    bx = b_r * st * cp + b_t * ct * cp - b_p * sp
    by = b_r * st * sp + b_t * ct * sp + b_p * cp
    bz = b_r * ct - b_t * st
    return np.stack([bx, by, bz], axis=1) * 1e-9


def igrf_field_eci(r_eci, time, coeffs, lmax=13):
    """Return the field in tesla, ECI axes, for (N, 3) ECI points."""
    b_ecef = igrf_field(eci_to_ecef(r_eci, time), coeffs, lmax)
    return ecef_to_eci(b_ecef, time)
