"""Condition-based schedule: which mode applies at each sample."""
import numpy as np

from darknessalp.frames.sun import sun_vector
from darknessalp.geometry.umbra import in_umbra


def conditions(time, r_eci, extra=None):
    """Return {name: bool (N,)} with umbra, sunlit, always, plus extra."""
    umbra = in_umbra(r_eci, sun_vector(time))
    out = {"umbra": umbra, "sunlit": ~umbra, "always": np.ones_like(umbra)}
    out.update(extra or {})
    return out


def select(rules, conds):
    """Return (mode_index (N,), modes) for [(condition, mode), ...]."""
    n = len(next(iter(conds.values())))
    index = np.full(n, -1)
    modes = [m for _, m in rules]
    for i, (cond, _) in enumerate(rules):
        index[(index < 0) & conds[cond]] = i
    if (index < 0).any():
        raise ValueError("no rule matched some samples; add ('always', m)")
    return index, modes
