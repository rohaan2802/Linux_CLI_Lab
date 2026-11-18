# Linux CLI Lab

## A reproducible command-line security portfolio

Mohammad Rohaan · 22I-2327 · CS-3002 Information Security

## Executive overview

This project develops the Linux fundamentals assignment into a repeatable local lab. Its maintained Python orchestrator executes real GNU/Linux tools inside a temporary directory, checks each result and writes a structured evidence file. A temporary loopback HTTP server supports download and upload exercises.

The original assignment has twelve assessed tasks. The maintained demo covers the file, text, batch, transfer and binary workflows with 24 checked exercises. Root sessions, package installation and host SSH lifecycle operations are documented in the administrative reference. The banking case study is a conceptual threat model.

## Project contents

- cli_lab/lab.py owns command execution, fixture validation, the temporary workspace and the local HTTP endpoint.
- cli_lab/addition.py demonstrates finite decimal input and owner-only permission handling.
- cli_lab/__main__.py exposes doctor, demo, verify and summary commands.
- cli_lab/evidence.py validates saved-run metadata and fixture-dependent results.
- data/fixtures/ contains the ten classroom files. data/manifest.json records their SHA-256 hashes.
- results/demo.json is the saved execution evidence used by the gallery.
- docs/original/ preserves the brief and the submitted report.
- docs/THREAT_MODEL.md and data/risk_register.csv describe the banking case study.

## Reproduction

Use Python 3.10 or newer in Linux, Ubuntu on WSL, or the course virtual machine. Required tools are bash, find, grep, tr, awk, xargs, xxd, curl, wget and stat.

    python3 -m cli_lab doctor
    python3 -m cli_lab demo
    python3 -m cli_lab verify
    python3 -m cli_lab summary
    python3 -m unittest discover -s tests -v

The demo stores commands, stdout, stderr, exit codes and checks. Durations measure one local run and are useful for tracing. The JSON evidence file is replaced atomically.

## Corrections and interpretation

The AWK dataset has four fields. The score is $4, so name:score uses $1 and $4. Its eight records have average 84.875.

Use tr classes such as [:digit:], [:alpha:] and [:xdigit:] for the relevant character sets. The demo sets LC_ALL=C for its ASCII examples.

Wget rate values are bytes per second. Decimal 1 Mbps corresponds to 125000 bytes per second. The tiny transfer fixture checks correctness and command handling.

Wget -N enables timestamp-based retrieval decisions. --append-output selects an appended diagnostic log. curl --trace-time supplies timestamps in traces. These are separate behaviors.

The xxd demonstration explicitly selects offset 0x0a. The grouped display uses -c 9 -g 3, which yields three groups of three bytes per row.

## Execution boundaries

All automated file changes take place within a temporary directory. The supplied fixtures remain unchanged and their checksums are verified before execution. Transfers use an ephemeral HTTP server bound to 127.0.0.1. No external target is contacted by the demo.

Administrative tasks require the intended VM environment and privileges. They are included as reference commands and original evidence; the saved demo does not claim a current privileged service test.

## Banking security case study

The original submission discusses an online banking application. The maintained threat model covers customer data, account records, sessions, transaction integrity, dependencies, audit logs and availability. The CSV supplies eight illustrative risks with proposed controls and verification actions. Their scores are design estimates.

Parameterized SQL addresses injection boundaries. Object-level authorization checks customer ownership. Idempotency protects against duplicate transactions. Session protection includes secure cookie flags, expiry and appropriate CSRF controls. Password storage requires a suitable password-hashing approach and migration policy.

## Evidence guide

The implementation chapters explain architecture, platform setup, fixture content, evidence validation, command workflows, banking risks, troubleshooting and the verification strategy. Their shared source is data/project_sections.json.

The following 24 figures show maintained-demo commands and captured results. Each figure is generated from the corresponding saved JSON step. The README and webpage use these same image files, captions and ordering.

The appendix preserves all 24 pages of the original submission at full-page size. Its historical terminal screenshots and commentary remain available alongside the maintained explanation.

## References

- GNU Coreutils manual: https://www.gnu.org/software/coreutils/manual/coreutils.html
- GNU Findutils xargs options: https://www.gnu.org/software/findutils/manual/html_node/find_html/xargs-options.html
- GNU Wget download options: https://www.gnu.org/software/wget/manual/html_node/Download-Options.html
- systemctl manual: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
- OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Password Storage: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

## About the author

Mohammad Rohaan · BS Computer Science, FAST-NUCES

GitHub: https://github.com/rohaan2802
Email: m.rohaanarshad@gmail.com
