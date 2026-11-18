# Command guide and task mapping

## Run the maintained demo

    python3 -m cli_lab doctor
    python3 -m cli_lab demo
    python3 -m unittest discover -s tests -v

The demo verifies fixture checksums, creates a fresh temporary workspace, starts an HTTP server on 127.0.0.1 and executes 24 checked exercises. Its temporary server and files are closed when execution completes. results/demo.json records commands, output, checks, environment and durations. Saved durations describe one run.

## Task mapping

| Course task | Maintained coverage | Evidence |
| --- | --- | --- |
| 1 Root identity | VM commands and verification notes | ADMIN_TASKS.md and original PDF |
| 2 apt and tree | VM commands; local transfer verification | ADMIN_TASKS.md and exercises 18–21 |
| 3 File operations | Create, write, append, copy, move and compare | Exercises 03–05 |
| 4 find, grep and Python | Scoped discovery, fields, decimal addition, chmod 700 | Exercises 04–06 |
| 5 tr | Digit/hex classes, case, vowels, spaces, squeeze and tabs | Exercises 07–11 |
| 6 awk | First/fourth fields, comma-separated names and score summary | Exercises 12–14 |
| 7 xargs | Filename batches, owner-read-only files, reconstructed list and NUL handling | Exercises 15–17 |
| 8 curl | Loopback request, custom user agent and verified upload | Exercises 18–19 |
| 9 wget | Download log, bytes, rate cap and timestamp-aware refresh | Exercises 20–21 |
| 10 xxd | Offset slice, grouped octets, flag and byte round-trip | Exercises 22–24 |
| 11 systemctl | Lifecycle and candidate configuration checks | ADMIN_TASKS.md and original PDF |
| 12 Banking security | Assets, trust boundaries, controls and risk register | THREAT_MODEL.md and risk_register.csv |

## Correct interpretation of the inputs

The AWK fixture has four fields: name, program, city and score. Name:score uses $1 and $4. The expected average score is 84.875 across eight records.

tr character classes include [:digit:], [:alpha:] and [:xdigit:]. Use LC_ALL=C for the ASCII-based examples. A class is clearer than a bracket expression borrowed from a regular expression language.

The xargs input includes -security_check.txt. Put -- before filename operands passed to touch and chmod. xargs -0 with NUL-delimited input preserves spaces and special characters. -n 1 limits each command invocation to one input argument.

The wordlist fixture paths are validated before they are read. The complete local reconstruction has 16 lines. This exercise uses only the supplied classroom data.

## Transfer units and logs

A decimal 1 Mbps is 1,000,000 bits per second, or 125,000 bytes per second. wget --limit-rate=125000 expresses that byte rate. Suffixes such as k and m use the tool's size conventions, so 1m represents a different rate from 1 Mbps.

wget --append-output=download.log appends its diagnostic log. --timestamping (or -N) controls timestamp-based retrieval decisions. curl --trace-time adds timing information to traces. curl -w can report structured timings such as time_total. Verbose output alone does not express every timestamp requirement.

The demo's small fixture verifies transfer correctness and command handling. It does not measure sustained bandwidth or promise an exact network throughput.

## Byte offsets

The maintained slice begins at offset 0x0a and includes 50 bytes. A human phrase such as tenth byte can also be interpreted as a one-based position; the report states the selected offset explicitly. xxd -c 9 -g 3 gives nine bytes per row arranged as three groups of three. Width and grouping control different aspects of the display.

## Historical and current evidence

The original report contains full-screen terminal evidence and a banking discussion. The current JSON and gallery describe a new reproducible Linux run. Privileged root/apt/SSH changes remain VM reference exercises and were not applied to the host in this project.
