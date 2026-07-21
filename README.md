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

## Project layout

- `src/darknessalp/`: package code
- `src/darknessalp/say_hello.py`: starter function example
- `src/darknessalp/__main__.py`: simple command-line entry point
- `src/routines/`: custom FORMS-native routines used by missions and notebooks
- `notebooks/`: all project notebooks, including the FORMS SDK mission examples
- `docs/`: reference material and notes
- `output/`: code-generated results and derived artifacts

## Next steps

Useful extensions once the scope sharpens:

- Replace the dipole field with IGRF or a higher-fidelity geomagnetic model
- Add eclipse, attitude, and duty-cycle constraints
- Model actual ALP signal response instead of a magnetic-exposure proxy
- Add launch/operations constraints to the optimization objective
