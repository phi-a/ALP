"""Rate-limited steering: the commanded attitude chases the desired one."""
import numpy as np
from scipy.spatial.transform import Rotation


def steer(desired, t_s, rate_deg_s=1.5, settle_deg=0.1, start=None,
          mode_index=None):
    """Return (commanded Rotations, error_deg, slewing) at a fixed rate."""
    t = np.asarray(t_s, float)
    n = len(t)
    quats = np.empty((n, 4))
    error = np.empty(n)
    moved = np.empty(n)
    current = desired[0] if start is None else start

    # a one-element stack would make every angle below an array
    current = Rotation.from_quat(np.ravel(current.as_quat()))
    for k in range(n):
        dt = t[k] - t[k - 1] if k else 0.0
        gap = desired[k] * current.inv()            # rotation still to do
        angle = float(np.degrees(gap.magnitude()))
        step = min(angle, rate_deg_s * dt)
        if angle > 1e-12:
            current = Rotation.from_rotvec(
                gap.as_rotvec() * step / angle) * current
        quats[k] = current.as_quat()
        error[k], moved[k] = angle - step, step

    # slewing: still behind, or moved more than tracking the same mode
    track = np.zeros(n)
    track[1:] = np.degrees((desired[1:] * desired[:-1].inv()).magnitude())
    if mode_index is not None:
        track[1:][np.diff(mode_index) != 0] = 0.0
    slewing = (error > settle_deg) | (moved > track + settle_deg)
    return Rotation.from_quat(quats), error, slewing
