# darknessALP

Minimal Python scaffold for orbit simulation and coarse CONOPS optimization for
LEO dark matter searches with an ALP-magnetic-field interaction proxy.

The initial model is intentionally simple:

- Two-body circular orbit initialization
- Earth-centered inertial propagation with fixed-step RK4
- Aligned dipole approximation for Earth's magnetic field
- Exposure metric based on integrated magnetic-field strength along the orbit
- Brute-force sweep over altitude and inclination

This is a starting point, not a validated mission physics model.

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

Run the example package:

```powershell
python -m darknessalp
```

Run tests:

```powershell
python -m unittest discover -s tests
```

Draw what the boresight sees:

```powershell
python plots/fov_view.py --target gc --epoch 2027-05-01T00:00:00 --t 4140 --out outputs/fov.png
```

## Project layout

- `src/darknessalp/`: package code, one function per file, stdlib
  - orbit and time: `circular_orbit` (J2 node rate), `julian_date`, `gmst`
  - frames: `eci_to_ecef`, `ecef_to_eci`, `ecef_to_spherical`,
    `radec_to_eci`, `galactic_to_radec`, `radec_to_galactic`
  - field: `load_igrf` (IGRF-14), `igrf_field`, `dipole_field`,
    `field_eci`, `schmidt_legendre`, `magnetic_latitude`, `cutoff_rigidity`
  - geometry: `los_field_integral`, `earth_limb_angle`, `in_umbra`,
    `sun_direction`, `fov_axes`, `project_to_fov`, `earth_limb_directions`
  - `bright_sources`: the brightest 2-10 keV sources for FOV checks
  - `fetch_axion_limit.py`, `list_axion_limits.py`: AxionLimits archive
  - `bfield/`, `yamamoto/`: legacy numpy code, used as test oracles
- `plots/`: matplotlib scripts (`fov_view.py`: the view from the boresight)
- `src/routines/`: FORMS routines, not used by the student path
- `jupyter/`: all notebooks (FORMS missions, Yamamoto 2020 Fig. 7, cohort)
- `Notebook/`: project notes and decisions — the second memory (tracked)
- `docs/`: papers, slides, drafts — references (not tracked)
- `data/`: model coefficients and cached limit files; `data/suzaku/` not tracked
- `freeflyer/`: FreeFlyer scripts
- `outputs/`: code-generated results (not tracked)

## Next steps

Useful extensions once the scope sharpens:

- Replace the dipole field with IGRF or a higher-fidelity geomagnetic model
- Add eclipse, attitude, and duty-cycle constraints
- Model actual ALP signal response instead of a magnetic-exposure proxy
- Add launch/operations constraints to the optimization objective
