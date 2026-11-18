"""Regression checks for hostile-looking filenames, malformed inputs and atomic evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from cli_lab.lab import ROOT, atomic_json, validate_fixture_paths
from cli_lab.evidence import inspect_evidence


class RegressionTests(unittest.TestCase):
    def addition(self, *values):
        return subprocess.run([sys.executable, str(ROOT / "cli_lab/addition.py"), *values],
                              capture_output=True, text=True)

    def test_decimal_precision(self):
        self.assertTrue(self.addition("0.1", "0.2").stdout.strip().endswith("0.3"))

    def test_non_finite_input_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity", "oops"):
            self.assertNotEqual(self.addition(value, "1").returncode, 0)

    def test_fixture_traversal_rejected(self):
        for value in ("../README.md", "/etc/passwd", "missing.txt"):
            with self.assertRaises(ValueError):
                validate_fixture_paths([value])

    def test_course_file_list(self):
        files = validate_fixture_paths(["parts/shortrockyou_01.txt", "parts/shortrockyou_02.txt"])
        self.assertEqual(len(files), 2)

    def test_atomic_result_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "result.json"
            atomic_json(path, {"checks": 1})
            atomic_json(path, {"checks": 2})
            self.assertEqual(json.loads(path.read_text()), {"checks": 2})
            self.assertEqual([x.name for x in path.parent.iterdir()], ["result.json"])

    def test_leading_dash_fixture_preserved(self):
        names = (ROOT / "data/fixtures/xarg_task.txt").read_text().splitlines()
        self.assertIn("-security_check.txt", names)

    def test_saved_evidence(self):
        self.assertEqual(inspect_evidence(ROOT / "results/demo.json")["exercises"], 24)

    def test_tampered_evidence_rejected(self):
        original = json.loads((ROOT / "results/demo.json").read_text())
        mutations = [
            lambda run: run["steps"].pop(),
            lambda run: run["steps"][11].update(stdout="Ali:999"),
            lambda run: run["steps"][0].update(duration_ms=float("nan")),
            lambda run: run["steps"][0].update(passed=False),
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            for mutate in mutations:
                run = json.loads(json.dumps(original))
                mutate(run)
                path.write_text(json.dumps(run))
                with self.assertRaises(ValueError):
                    inspect_evidence(path)


if __name__ == "__main__":
    unittest.main()
