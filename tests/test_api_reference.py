"""The generated API reference must cover the package and stay current."""
import inspect
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import darknessalp as d

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "Notebook" / "02-mission-analysis" / "api-reference.md"
SCRIPT = ROOT / "scripts" / "api_reference.py"


def public_api():
    """Return [(topic, name)] for every exported name in every topic."""
    return [(topic, name) for topic in d.__all__
            if inspect.ismodule(getattr(d, topic, None))
            for name in getattr(getattr(d, topic), "__all__", [])]


class TestApiReference(unittest.TestCase):
    def test_every_public_name_appears(self):
        text = NOTE.read_text(encoding="utf-8")
        for topic, name in public_api():
            self.assertIn(f"`{name}", text, f"{topic}.{name} undocumented")

    def test_every_function_has_a_docstring(self):
        for topic, name in public_api():
            obj = getattr(getattr(d, topic), name)
            if callable(obj):
                self.assertTrue(inspect.getdoc(obj), f"{topic}.{name}")

    def test_note_is_current(self):
        with TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "api.md"
            subprocess.run([sys.executable, str(SCRIPT), str(fresh)],
                           cwd=ROOT, check=True)
            self.assertEqual(fresh.read_text(encoding="utf-8"),
                             NOTE.read_text(encoding="utf-8"),
                             "regenerate: python scripts/api_reference.py "
                             "Notebook/02-mission-analysis/api-reference.md")


if __name__ == "__main__":
    unittest.main()
