"""Linear Poisson model mu = sum_a theta_a t_a: information, errors, fits."""
import numpy as np
from scipy.stats import norm


def _rows(templates):
    return np.asarray([np.ravel(t) for t in templates], float)


def fisher(templates, mu):
    """Return I_ab = sum over cells of t_a t_b / mu."""
    t = _rows(templates)
    return (t / np.ravel(mu)) @ t.T


def profiled_sigma(signal, nuisance, mu):
    """Return the error on the signal amplitude after profiling nuisance."""
    return float(np.sqrt(np.linalg.inv(fisher([signal, *nuisance], mu))[0, 0]))


def information_fraction(signal, nuisance, mu):
    """Return the share of the signal's information that survives profiling."""
    info = fisher([signal, *nuisance], mu)
    return float(1.0 / (info[0, 0] * np.linalg.inv(info)[0, 0]))


def upper_limit(sigma, cl=0.9):
    """Return the one-sided Gaussian upper limit on a null amplitude."""
    return norm.ppf(cl) * np.asarray(sigma)


def fit_amplitudes(counts, templates, mu):
    """Return least-squares amplitudes with weights 1/mu."""
    t = _rows(templates)
    w = t / np.ravel(mu)
    return np.linalg.solve(w @ t.T, w @ np.ravel(counts))
