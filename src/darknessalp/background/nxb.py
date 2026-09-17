"""Particle (non-X-ray) background proxy from cut-off rigidity (ASSUME)."""
import numpy as np


def nxb_proxy(cutoff_gv, index=1.0, reference_gv=10.0):
    """Return a relative NXB level, 1 at reference_gv, scaling Rc^-index."""
    rc = np.clip(np.asarray(cutoff_gv, float), 0.5, None)
    return (rc / reference_gv) ** -index
