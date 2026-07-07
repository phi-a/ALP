"""sdk_routine.py -- a FORMS *routine*: a function that takes the ``forms`` handle.

A **brick** is a pure function of numbers; a **routine** is a function that takes
``forms``, reads mission state off the handle, and composes bricks. That handle
argument is the whole difference -- it is what lets a routine reach live mission
state a pure brick never sees.

The engine already *derives* the common quantities (``alt``, ``sma``, ``BGCRS``,
...), so a routine is worth writing when it computes something the engine does
not publish. This worked routine records the separation between two Orrery
particles -- a quantity that only exists once you have a multi-particle manifest.
Because it runs every propagator step, it is written as a *factory*: call
``track_gap(f, "probe", "debris")`` once to register the output variable, and it
returns a zero-argument ``sample`` you bind to ``SequenceRunner(tick=...)``. The
engine's per-step ``record`` phase then writes the marked variable to the mission
CSV automatically -- no manual file writing.

Copy and rename this file for each calculation of your own. A one-shot routine is
even simpler -- just ``def my_quantity(forms): ...`` that reads the handle, calls
bricks, and returns a value.
"""

from __future__ import annotations


def track_gap(forms, a="probe", b="debris", *, var="sep_km"):
    """Make a per-step routine that records the range between two particles.

    Parameters
    ----------
    forms :
        The ``forms`` handle the mission was configured on.
    a, b : str
        Names of two particles in the built ``forms.orrery`` manifest.
    var : str
        Name of the scalar variable to record the separation into (km).

    Returns
    -------
    Callable[[], None]
        A zero-argument ``sample`` to bind to ``SequenceRunner(tick=...)``.
    """
    # A marked scalar variable -> the engine's record phase writes it to CSV.
    gap = forms.get_variable(var) or forms.types.scalar(var, 0.0, unit="km")
    gap.mark()

    def sample() -> None:
        """Compute and store the a-b range for the current step."""
        ra = forms.orrery.state(a)               # flat [x, y, z, vx, vy, vz], km
        rb = forms.orrery.state(b)
        gap.set(sum((ra[i] - rb[i]) ** 2 for i in range(3)) ** 0.5)

    return sample
