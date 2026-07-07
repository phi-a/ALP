"""example_mission.py -- a FORMS *mission script* (the house style).

A **mission** is a full, runnable simulation: configure the ``forms`` handle, set
the scenario, propagate it, and report the result. Mission scripts live in
``missions/`` -- one file per scenario, with a descriptive name
(``leo_formation.py``, ``ground_track_survey.py``, ...). Copy this file and rename
it for each new mission.

Follow this shape: a CONFIGURATION block of constants, then ``build`` -> ``run``
-> ``report``, driven by ``main``. Plots use matplotlib (bundled with the SDK);
never hand-roll image or file encoding. A *routine* (``routines/``) is a small,
reusable calculation on ``forms`` -- this mission imports one (``track_gap``)
rather than re-deriving it. Keep whole simulations out of ``routines/``.

Before extending this, learn the API from inside the package (see AGENTS.md):
``forms.FORMS().api_search("...")`` for the exact call, ``book_ai("...")`` for the
model. Run it:  python missions/example_mission.py
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

# Put the workspace root on the path so ``routines`` imports resolve however the
# script is launched. This reaches your OWN workspace code, not installed forms.
WORKSPACE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE))

import forms
from forms.sequence import ListSink, Segment, Sequence, SequenceRunner

from routines.sdk_routine import track_gap

# --- CONFIGURATION ---------------------------------------------------------
EPOCH = "2026:01:01:00:00:00"
SMA_KM = 6928.0            # ~550 km altitude
ECC, INC_DEG = 0.001, 51.6
RAAN_DEG, AOP_DEG, TA_DEG = 30.0, 40.0, 0.0
COMPANION_OFFSET_KM = 10.0  # cross-track offset of the second particle
STEP_S = 60.0
OUTPUTS = WORKSPACE / "outputs"


def build(f):
    """Configure a two-particle LEO Orrery; return the fixed step (seconds)."""
    f.load_koe(a=SMA_KM, e=ECC, i=INC_DEG, raan=RAAN_DEG, aop=AOP_DEG, ta=TA_DEG,
               timestamp=EPOCH, mu=f.planet.mu)
    y0 = f.satellite.get_state()

    # The Orrery is FORMS' multi-body manifest: a center, perturbing sources, and
    # integrated particles. The particle marked satellite=True is the one the
    # handle's orbit / lla / eclipse / derive phase follow.
    f.orrery.set_center("earth").add_source("sun").add_source("moon")
    f.orrery.add_particle("probe", y0, satellite=True)
    companion = list(y0)
    companion[1] += COMPANION_OFFSET_KM
    f.orrery.add_particle("companion", companion)

    f.time.set_span(mode="simulated", duration=float(f.orbit.period), units="seconds")
    f.orrery.build(fixed_dt=STEP_S)

    f.set_record_directory(str(OUTPUTS))
    for name in ("alt", "sma", "InUmbra"):
        f.get_variable(name).mark()


def run(f):
    """Propagate one orbit, sampling a routine each step; return the result."""
    sample_gap = track_gap(f, "probe", "companion", var="sep_km")  # a reusable routine
    sequence = Sequence(name="example_mission", segments=(
        Segment("setup", {}, label="initialize state"),
        Segment("propagate", {}, label="propagate one orbit"),
    ))
    return SequenceRunner(f, sequence, sink=ListSink(), tick=sample_gap).run()


def report(f, result):
    """Plot altitude, and write a JSON summary of the run."""
    import matplotlib
    matplotlib.use("Agg")  # headless: write a PNG without needing a display
    import matplotlib.pyplot as plt

    rows = list(csv.DictReader(open(f.recorder.file_path, newline="")))
    t_min = [i * STEP_S / 60.0 for i in range(len(rows))]
    alt = [float(r["alt"]) for r in rows]
    gap = [float(r["sep_km"]) for r in rows]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t_min, alt)
    ax.set_xlabel("time [min]"); ax.set_ylabel("altitude [km]")
    ax.set_title("Satellite altitude over one orbit")
    fig.tight_layout()
    plot_path = OUTPUTS / "example_mission_altitude.png"
    fig.savefig(plot_path, dpi=120)

    umbra = f.events.eclipse_summaries_for_orbits(step_s=STEP_S, kinds=("umbra",))[0]
    summary = {
        "steps": result.steps,
        "altitude_km": {"min": min(alt), "max": max(alt)},
        "max_probe_companion_gap_km": max(gap),
        "umbra": {"windows": umbra.window_count, "duty_cycle": umbra.duty_cycle},
        "outputs": {"record_csv": str(f.recorder.file_path), "plot_png": str(plot_path)},
    }
    summary_path = OUTPUTS / "example_mission_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"{result.name}: {result.steps} steps -> {f.recorder.file_path}")
    print(f"umbra: {umbra.window_count} window(s), {100 * umbra.duty_cycle:.1f}% duty")
    print(f"plot: {plot_path}")
    print(f"summary: {summary_path}")


def main():
    f = forms.FORMS()
    build(f)
    result = run(f)
    report(f, result)


if __name__ == "__main__":
    main()
