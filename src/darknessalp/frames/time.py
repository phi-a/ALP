"""Epoch handling: seconds after an epoch -> astropy Time."""
import numpy as np
from astropy.time import Time, TimeDelta


def times(epoch, t_s):
    """Return astropy Time for seconds after a datetime or ISO epoch."""
    return Time(epoch) + TimeDelta(np.atleast_1d(t_s), format="sec")


def decimal_year(time):
    """Return the decimal year of a Time (scalar or array)."""
    return time.decimalyear
