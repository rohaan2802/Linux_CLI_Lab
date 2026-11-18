## Source and Execution Workflow

The runnable project starts at cli_lab/__main__.py. The command router selects an environment check, a fresh demo, or an inspection of existing evidence.

| Source file | Responsibility | Review focus |
| --- | --- | --- |
| cli_lab/lab.py | Temporary workspace, GNU tool execution and loopback server | Quoted operands, exit codes, output checks and cleanup |
| cli_lab/addition.py | Finite decimal inputs and addition | Invalid input handling and decimal output |
| cli_lab/evidence.py | Saved-run validation and readable summaries | Ordered exercises, fixture hashes and result consistency |
| tools/build_showcase.py | Shared figures, README, webpage and report | One figure manifest and reproducible output sizes |
| tools/verify_showcase.py | Presentation and appendix verification | File paths, matching gallery order and original pages |
| tests/test_lab.py | Regression coverage | Corrupt evidence, file paths, atomic writes and numeric inputs |

### Inspect a saved run on Windows or Linux

    python -m cli_lab verify
    python -m cli_lab summary

These commands inspect saved evidence without running the Linux exercises. verify checks hashes, required metadata and fixture-dependent results. summary shows exercise counts by category and a SHA-256 digest for the evidence file.

The evidence format is documented in [Evidence Contract](EVIDENCE_CONTRACT.md). Checks establish consistency with the included fixtures. The JSON file is editable local evidence, so its digest identifies content rather than proving authorship.

### What happens during a fresh demo

1. Check that the required Linux tools are available.
2. Verify the input fixtures and the paths used by the classroom file lists.
3. Create a fresh temporary workspace and copy the required inputs.
4. Start a server bound to 127.0.0.1 on an available port.
5. Execute each command with a timeout and an explicit expected-output check.
6. Close the server, remove temporary files and atomically save the result.

## Reading the Results

The score average comes from eight supplied records, with scores in the fourth field. The local HTTP upload is checked byte for byte. The downloaded 37-byte fixture is compared with its source. The binary exercise converts the supplied bytes to hex and back before comparing the result.

A command's zero exit code is recorded alongside its expected-output check. The saved log also contains stderr, which includes xargs verbose traces where relevant. Gallery captures emphasize the command and stdout; the JSON preserves the full recorded fields.

## Reviewer Walkthrough

Start with the [portfolio report](Linux_CLI_Lab_Report.pdf), then inspect a gallery figure and its corresponding JSON step. Run summary to inspect the saved counts, and verify to check the fixture/result relationship. In Linux, run demo for fresh evidence and the regression suite for the failure cases.

The [command guide](TASK_GUIDE.md) maps the maintained demo to all twelve course tasks. [VM administration notes](ADMIN_TASKS.md) cover root, apt and SSH lifecycle operations. The [banking threat model](THREAT_MODEL.md) connects assets, proposed controls and verification ideas.

