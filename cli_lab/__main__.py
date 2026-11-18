"""Command-line entry point for Linux CLI Lab."""
import argparse
import json
import subprocess
from pathlib import Path
from .lab import atomic_json, doctor, execute_demo
from .evidence import inspect_evidence, summary_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["doctor", "demo", "verify", "summary"])
    parser.add_argument("--output", type=Path, default=Path.cwd() / "results/demo.json")
    parser.add_argument("--evidence", type=Path, default=Path.cwd() / "results/demo.json")
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            result = doctor()
            print(json.dumps(result, indent=2))
            return 0 if result["ready"] else 1
        if args.command in ("verify", "summary"):
            report = inspect_evidence(args.evidence)
            print(summary_text(report) if args.command == "summary" else json.dumps(report, indent=2))
            return 0
        result = execute_demo()
        atomic_json(args.output, result)
        print(f"{result['checks_passed']} checked exercises passed")
        print(f"Evidence written to {args.output}")
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
