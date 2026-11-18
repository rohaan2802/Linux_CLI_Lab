# Evidence contract

results/demo.json is the saved record used by the portfolio. Its schema_version is 1.

## Run fields

| Field | Meaning |
| --- | --- |
| project | Linux_CLI_Lab |
| schema_version | Evidence representation version |
| recorded_at | UTC timestamp for the saved execution |
| environment | Python/platform information and tool availability |
| checks_passed | Number of successful exercises |
| scope | Description of the local execution boundary |
| steps | Ordered command evidence from 01 through 24 |

## Exercise fields

Each step records id, title, category, command, stdout, stderr, returncode, passed and duration_ms. stdout is the output inspected by the exercise check. stderr retains diagnostics such as xargs traces. The record normalizes the temporary directory name to <workspace>.

## Validation

    python -m cli_lab verify
    python -m cli_lab summary

The validator checks the schema, project name, ordered unique exercise IDs, required text, successful exit/check fields and finite non-negative timings. It verifies fixture hashes and compares the AWK and reconstructed-wordlist results with the actual fixture content. It also checks recorded permissions, transfer length and the training flag.

The SHA-256 digest identifies the precise JSON bytes. Authentic execution still depends on the runner and its surrounding environment. This format supplies reproducible local evidence and does not provide a digital signature.

## Failure cases

A missing step, failed result, invalid timing or changed fixture-dependent output causes a nonzero CLI exit. A missing or modified fixture also prevents successful validation. A readable summary is produced only after the same checks pass.

## Updating evidence

Run the demo from the project root, inspect its results, then rebuild the showcase. If the fixture data changes intentionally, review the expected-output checks and manifest together. Regenerate the site and report so their visible results correspond to the reviewed evidence.
