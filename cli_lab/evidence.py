"""Validate saved run structure and fixture-dependent results."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from .lab import FIXTURES, verify_fixtures


def inspect_evidence(path):
    raw = Path(path).read_bytes()
    run = json.loads(raw)
    if not isinstance(run, dict):
        raise ValueError("evidence must be a JSON object")
    if run.get("schema_version") != 1 or run.get("project") != "Linux_CLI_Lab":
        raise ValueError("unsupported evidence schema or project")
    steps = run.get("steps", [])
    if not isinstance(steps, list) or not all(isinstance(step, dict) for step in steps):
        raise ValueError("steps must be a list of exercise records")
    if not isinstance(run.get("recorded_at"), str):
        raise ValueError("evidence must include a recording timestamp")
    ids = [step.get("id") for step in steps]
    if ids != [f"{number:02}" for number in range(1, 25)]:
        raise ValueError("evidence must contain exercises 01 through 24 in order")
    for step in steps:
        if step.get("passed") is not True or (type(step.get("returncode")) is not int or step["returncode"] != 0):
            raise ValueError(f"exercise {step['id']} did not pass")
        if not all(isinstance(step.get(key), str) and step[key] for key in ("title", "category", "command", "stdout")):
            raise ValueError(f"exercise {step['id']} has incomplete evidence")
        duration = step.get("duration_ms")
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration < 0:
            raise ValueError(f"exercise {step['id']} has invalid timing")
    if run.get("checks_passed") != 24:
        raise ValueError("reported exercise total does not match the evidence")
    by_id = {step["id"]: step for step in steps}
    expected_scores = "\n".join(f"{row.split()[0]}:{row.split()[3]}" for row in (FIXTURES / "awk_task.txt").read_text().splitlines())
    expected_words = "".join((FIXTURES / "parts" / f"shortrockyou_{number:02}.txt").read_text() for number in range(1, 5)).strip()
    if by_id["12"]["stdout"] != expected_scores or by_id["16"]["stdout"] != expected_words:
        raise ValueError("saved text results differ from the supplied fixtures")
    modes = by_id["15"]["stdout"].splitlines()
    if len(modes) != 5 or any(not line.startswith("400 ") for line in modes):
        raise ValueError("saved batch permissions are inconsistent")
    if by_id["20"]["stdout"] != "download bytes verified\n37":
        raise ValueError("saved transfer result is inconsistent")
    if "flag{xxd_offset_master_2026}" not in by_id["24"]["stdout"]:
        raise ValueError("saved binary result is inconsistent")
    fixture_count = verify_fixtures()
    return {
        "exercises": len(steps), "fixtures": fixture_count,
        "categories": dict(sorted(Counter(step["category"] for step in steps).items())),
        "recorded_at": run["recorded_at"], "sha256": hashlib.sha256(raw).hexdigest(),
    }


def summary_text(result):
    lines = [
        "Linux CLI Lab / saved evidence summary",
        f"Recorded: {result['recorded_at']}",
        f"Verified exercises: {result['exercises']}",
        f"Verified fixtures: {result['fixtures']}",
        "",
    ]
    lines.extend(f"{category}: {count}" for category, count in result["categories"].items())
    lines.extend(["", f"Evidence SHA-256: {result['sha256']}"])
    return "\n".join(lines)
