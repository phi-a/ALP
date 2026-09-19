"""Write the API reference note from the package docstrings."""
import argparse
import inspect
import re

import darknessalp as d

FUNC_DEFAULT = re.compile(r"<function (\w+) at 0x[0-9A-Fa-f]+>")
PATH_DEFAULT = re.compile(r"(?:Windows|Posix)Path\('.*?/(data/[^']*)'\)")

BLURB = {
    "frames": "Time and reference frames. astropy does the work.",
    "orbit": "Where the spacecraft is.",
    "dynamics": "Accelerations and torques. Models only, no integration.",
    "kinematics": "Body attitude, slews, and rate-limited steering.",
    "pointing": "What to look at, and when.",
    "field": "The geomagnetic field and magnetic coordinates.",
    "geometry": "Lines of sight, the Earth disk, and the field of view.",
    "background": "Celestial and particle background models.",
    "sim": "The per-sample record every run produces.",
}


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("out", help="markdown path to write")
    return p.parse_args()


def rows(topic):
    """Return (signature, one-line docstring) for a topic's public API."""
    module = getattr(d, topic)
    out = []
    for name in module.__all__:
        obj = getattr(module, name)
        if not callable(obj):
            out.append((f"`{name}`", f"constant: {_summary(obj)}"))
            continue
        sig = FUNC_DEFAULT.sub(r"\1", str(inspect.signature(obj)))
        sig = PATH_DEFAULT.sub(r"'\1'", sig)
        doc =(inspect.getdoc(obj) or "").split("\n")[0]
        out.append((f"`{name}{sig}`", doc))
    return out


def _summary(value):
    if isinstance(value, dict):
        return "{" + ", ".join(sorted(value)) + "}"
    if isinstance(value, (list, tuple)):
        return f"{len(value)} entries"
    return repr(value)


def main():
    args = parse_args()
    lines = ["---", "type: reference",
             "tags: [darkness, alp, tooling, api]", "created: 2026-09-17",
             "updated: 2026-09-17", "status: active", "---", "",
             "# API reference", "",
             "Every public function in `src/darknessalp/`, with its",
             "signature and docstring. **Generated** — do not edit by hand:",
             "", "```powershell",
             "python scripts/api_reference.py "
             "Notebook/02-mission-analysis/api-reference.md", "```", "",
             "Conventions: positions in km, fields in tesla, angles in",
             "degrees, time as an astropy `Time`. Arrays are `(N, 3)` for",
             "vectors and `(N,)` for scalars; a single row is accepted",
             "wherever `(N, 3)` is.", ""]
    for topic in sorted(BLURB):
        lines += [f"## `{topic}`", "", BLURB[topic], "",
                  "| Call | Returns |", "|---|---|"]
        lines += [f"| {sig} | {doc} |" for sig, doc in rows(topic)]
        lines.append("")
    lines += ["## Links", "", "- part of [[../ALP]]",
              "- why these exist: [[tooling]], [[pointing-system]]",
              "- the run file: `jupyter/darkness_alp_sim.ipynb`", ""]
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


if __name__ == "__main__":
    main()
