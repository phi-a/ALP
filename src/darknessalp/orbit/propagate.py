"""Numerical propagation of a GCRF state with scipy solve_ivp."""
import numpy as np
from scipy.integrate import solve_ivp

from darknessalp.dynamics.orbital import two_body, two_body_j2

GRAVITY = {"point": two_body, "j2": two_body_j2}


def propagate(r0, v0, t_s, gravity="j2"):
    """Return r (N, 3) km and v (N, 3) km/s at t_s >= 0 s after the epoch."""
    accel = GRAVITY[gravity] if isinstance(gravity, str) else gravity
    t = np.atleast_1d(t_s).astype(float)
    y0 = np.concatenate([np.ravel(r0), np.ravel(v0)])
    if t.max() == 0:                      # nothing to integrate
        return np.tile(y0[:3], (len(t), 1)), np.tile(y0[3:], (len(t), 1))

    def rhs(_, y):
        return np.concatenate([y[3:], accel(y[:3])[0]])

    sol = solve_ivp(rhs, (0.0, t.max()), y0, t_eval=t, method="DOP853",
                    rtol=1e-10, atol=1e-12)
    return sol.y[:3].T, sol.y[3:].T
