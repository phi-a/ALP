# darknessALP

Minimal Python scaffold for orbit simulation and coarse CONOPS optimization for
LEO dark matter searches with an ALP-magnetic-field interaction proxy.

The model, as of 2026-09-17:

- Circular orbit with J2 secular rates, or numerical propagation (scipy)
- Astropy time and GCRS/ITRS frames, Sun, Galactic coordinates
- IGRF-14 geomagnetic field, vectorised, with the dipole as `lmax=1`
- Line-of-sight transverse field integral per ray, with Earth occultation
- Umbra, limb angle, Sun angle, magnetic latitude, Stormer cutoff rigidity
- Analytic CXB, Galactic ridge, NXB proxy, bright-source list
- A state table per pointing law, and the boresight view figure

## Quick start

Create a virtual environment and install the working environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

This installs the local project plus notebook tooling and the `FORMS` Python
package directly from GitHub.

If PowerShell blocks activation, use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run the simulation: open `jupyter/darkness_alp_sim.ipynb` and run all cells.

Run tests:

```powershell
python -m unittest discover -s tests
```

Draw what the boresight sees:

```powershell
python scripts/fov_view.py --target gc --epoch 2027-05-01T00:00:00 --t 4140 --out outputs/fov.png
```

## Project layout

- `src/darknessalp/` — the simulation library, numpy/scipy/astropy,
  functions on arrays, one subpackage per topic:
  - `frames/` time and reference frames (astropy): `times`, `eci_to_ecef`,
    `sun_vector`, `galactic_vector`, `to_galactic`
  - `orbit/` analytic circular + J2 (`circular_orbit`), `propagate` (scipy)
  - `dynamics/` accelerations (`two_body`, `j2_acceleration`)
  - `kinematics/` body attitude (`look_at`, `boresight`), slews
  - `pointing/` `target`, `feasible`, pointing laws
  - `field/` IGRF-14 (`load_igrf`, `igrf_field`, `igrf_field_eci`), dipole,
    `magnetic_latitude`, `cutoff_rigidity`
  - `geometry/` `los_field_integral` (vectorised over rays), `limb_angle`,
    `in_umbra`, FOV projection and cone quadrature
  - `background/` CXB, GRXE, NXB proxy, bright sources
  - `sim/` `state_table`, `to_csv`
  - `bfield/`, `yamamoto/` legacy code kept as test oracles
- `jupyter/darkness_alp_sim.ipynb` — **the run file**: builds one day of
  an ISS-like orbit with a fixed target, writes the state table, plots the
  orbit strip and the boresight view
- `scripts/` — thin argparse tools (`fov_view.py`)
- `tests/` — one file per topic; `python -m unittest discover -s tests`
- `Notebook/` notes (tracked); `docs/` references (untracked); `data/`
  inputs; `freeflyer/`; `outputs/` generated (untracked)

## Next steps

- Per-target correlation map of K against cutoff rigidity and limb angle
- Pointing schedules (two fixed targets, field-tracking) in `pointing/`
- Attitude dynamics and radiator/Sun constraints in `dynamics/`, `kinematics/`
- CHAOS field model comparison
