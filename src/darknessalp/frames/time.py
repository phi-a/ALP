"""Epoch handling: seconds after an epoch -> astropy Time."""
import numpy as np
from astropy.time import Time, TimeDelta


def times(epoch, t_s):
    """Return Time for seconds after an ISO, Julian-date or Time epoch."""
    if isinstance(epoch, (int, float)):      # a Julian date, UTC
        epoch = Time(epoch, format="jd", scale="utc")
    return Time(epoch) + TimeDelta(np.atleast_1d(t_s), format="sec")


def decimal_year(time):
    """Return the decimal year of a Time (scalar or array)."""
    return time.decimalyear
