from math import cos, sin, sqrt

from darknessalp.constants import R_EARTH_KM
from darknessalp.field_eci import field_eci


def los_field_integral(r_eci_km, n_hat, gmst_deg, coeffs, lmax=13,
                       q_per_m=0.0, l_max_re=10.0, n_steps=200):
    """Return |A| in T m with the running total along the line of sight."""
    x, y, z = r_eci_km
    nx, ny, nz = n_hat
    along = x * nx + y * ny + z * nz
    r2 = x * x + y * y + z * z

    # stop at the Earth surface when looking down, else at l_max_re
    disc = along**2 - r2 + R_EARTH_KM**2
    occulted = along < 0.0 and disc >= 0.0
    if occulted:
        s_end = -along - sqrt(disc)
    else:
        s_end = -along + sqrt(along**2 - r2 + (l_max_re * R_EARTH_KM) ** 2)

    ds = s_end / n_steps
    total = [0j, 0j, 0j]
    previous = None
    s_km, running_tm = [], []
    for k in range(n_steps + 1):
        s = k * ds
        point = (x + s * nx, y + s * ny, z + s * nz)
        b = field_eci(point, gmst_deg, coeffs, lmax)
        b_along = b[0] * nx + b[1] * ny + b[2] * nz
        phase = complex(cos(q_per_m * s * 1e3), sin(q_per_m * s * 1e3))
        current = [(b[i] - b_along * n_hat[i]) * phase for i in range(3)]
        if previous is not None:
            for i in range(3):
                total[i] += 0.5 * (previous[i] + current[i]) * ds * 1e3
        previous = current
        s_km.append(s)
        running_tm.append(sqrt(sum(abs(t) ** 2 for t in total)))

    return {"amplitude_tm": running_tm[-1], "vector_tm": tuple(total),
            "s_km": s_km, "running_tm": running_tm, "occulted": occulted}
