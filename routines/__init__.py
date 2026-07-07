"""Mission routines for this workspace.

A *routine* is a function that takes the ``forms`` handle: it reads live mission
state and composes pure bricks into a result. (A **brick** is a pure function of
numbers; the handle argument is the whole difference -- it is what lets a routine
reach mission state a brick never sees.) A routine earns its keep by computing
something the engine's ``derive`` phase does *not* already publish. Call it
directly for a one-shot value, or -- to run it every integration step -- bind the
callable it returns to the SequenceRunner's ``tick=`` hook. ``sdk_routine.py`` is
a worked example; copy and rename it for your own.

See sdk_quickstart.ipynb for the worked example end to end.
"""

from .sdk_routine import track_gap

__all__ = ["track_gap"]
