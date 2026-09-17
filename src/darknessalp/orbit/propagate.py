"""Numerical propagation of an ECI state with scipy solve_ivp."""
import numpy as np
from scipy.integrate import solve_ivp

from darknessalp.dynamics.orbital import two_body_j2


def propagate(r0, v0, t_s, acceleration=two_body_j2):
    """Return r (N, 3) and v (N, 3) at times t_s from an initial state."""
    def rhs(_, y):
        return np.concatenate([y[3:], acceleration(y[:3])[0]])

    t = np.atleast_1d(t_s).astype(float)
    sol = solve_ivp(rhs, (t[0], t[-1]), np.concatenate([r0, v0]),
                    t_eval=t, method="DOP853", rtol=1e-10, atol=1e-12)
    return sol.y[:3].T, sol.y[3:].T
