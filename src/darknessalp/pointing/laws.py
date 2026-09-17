"""Pointing laws: boresight per time sample, (N, 3)."""
import numpy as np


def fixed_inertial(target_hat, n_samples):
    """Return the same inertial boresight at every sample."""
    return np.tile(np.asarray(target_hat, float), (n_samples, 1))


def zenith(r_eci):
    """Return the local zenith at each (N, 3) position."""
    r = np.atleast_2d(r_eci)
    return r / np.linalg.norm(r, axis=1, keepdims=True)
