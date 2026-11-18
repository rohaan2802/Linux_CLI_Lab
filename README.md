<div align="center">

# Linux CLI Lab

**Reproducible Linux fundamentals, command-line evidence and a banking threat model.**

[![Python](https://img.shields.io/badge/Python-145E6B?style=for-the-badge&logo=python&logoColor=white)](cli_lab/lab.py)
[![GNU_Linux](https://img.shields.io/badge/GNU_Linux-145E6B?style=for-the-badge&logo=linux&logoColor=white)](docs/TASK_GUIDE.md)
[![Bash](https://img.shields.io/badge/Bash-145E6B?style=for-the-badge&logo=gnubash&logoColor=white)](Makefile)
[![Evidence_Audit](https://img.shields.io/badge/Evidence_Audit-145E6B?style=for-the-badge&logo=checkmarx&logoColor=white)](cli_lab/evidence.py)
[![JSON_Results](https://img.shields.io/badge/JSON_Results-145E6B?style=for-the-badge&logo=json&logoColor=white)](results/demo.json)
[![Regression_Tests](https://img.shields.io/badge/Regression_Tests-145E6B?style=for-the-badge&logo=python&logoColor=white)](tests/test_lab.py)
[![Rebuildable_Report](https://img.shields.io/badge/Rebuildable_Report-145E6B?style=for-the-badge&logo=readthedocs&logoColor=white)](tools/build_showcase.py)
[![24_Checked_Exercises](https://img.shields.io/badge/24_Checked_Exercises-145E6B?style=for-the-badge&logo=checkmarx&logoColor=white)](results/demo.json)
[![PDF_Report](https://img.shields.io/badge/PDF_Report-145E6B?style=for-the-badge&logo=readthedocs&logoColor=white)](docs/Linux_CLI_Lab_Report.pdf)
[![Security_Case_Study](https://img.shields.io/badge/Security_Case_Study-145E6B?style=for-the-badge&logo=owasp&logoColor=white)](docs/THREAT_MODEL.md)

</div>

## Live Links

| What | Link |
| --- | --- |
| Repository | [https://github.com/rohaan2802/Linux_CLI_Lab](https://github.com/rohaan2802/Linux_CLI_Lab) |
| GitHub Pages | [https://rohaan2802.github.io/Linux_CLI_Lab/](https://rohaan2802.github.io/Linux_CLI_Lab/) |
| GNU command reference | [https://www.gnu.org/software/coreutils/manual/coreutils.html](https://www.gnu.org/software/coreutils/manual/coreutils.html) |

## Contents

- [Overview](#overview)
- [What's Inside](#whats-inside)
- [Project Breakdown](#project-breakdown)
- [Folder Structure](#folder-structure)
- [Setup and Demo](#setup-and-demo)
- [Results](#results)
- [Source and Execution Workflow](#source-and-execution-workflow)
- [Reading the Results](#reading-the-results)
- [Reviewer Walkthrough](#reviewer-walkthrough)
- [Figures](#figures)
- [Limitations](#limitations)
- [About the Author](#about-the-author)
- [Architecture and Responsibilities](#architecture-and-responsibilities)
- [Reproduction and Platform Guide](#reproduction-and-platform-guide)
- [Fixture Catalog and Data Interpretation](#fixture-catalog-and-data-interpretation)
- [Evidence Lifecycle and Validation](#evidence-lifecycle-and-validation)
- [Command Workflows and Expected Results](#command-workflows-and-expected-results)
- [Banking Risk Review and Verification Ideas](#banking-risk-review-and-verification-ideas)
- [Troubleshooting and Failure Behavior](#troubleshooting-and-failure-behavior)
- [Testing Strategy and Review Checklist](#testing-strategy-and-review-checklist)

## Overview

A repeatable Linux command-line security lab built around CS-3002 coursework. The project runs 24 checked exercises across file operations, permissions, text processing, safe batch filenames, loopback transfers and binary inspection. A banking threat model connects the command-line work with application security.

## What's Inside

- [Portfolio PDF](docs/Linux_CLI_Lab_Report.pdf)
- [Report source](docs/Report.md)
- [Evidence contract](docs/EVIDENCE_CONTRACT.md)
- [Project handbook](docs/PROJECT_HANDBOOK.md)
- [Command guide](docs/TASK_GUIDE.md)
- [CLI source](cli_lab/lab.py)
- [Build file](Makefile)
- [Saved execution](results/demo.json)
- [Threat model](docs/THREAT_MODEL.md)
- [Risk register](data/risk_register.csv)
- [Assignment brief](docs/original/Assignment_Brief.pdf)
- [Original submission](docs/original/Original_Submission.pdf)
- [Original inventory](docs/INVENTORY.md)

## Project Breakdown

The Python runner verifies fixture checksums, creates a temporary workspace and invokes the real Linux tools with a C locale. Every step has an explicit output check. It closes its local HTTP server and temporary files after completion, then writes JSON evidence atomically.

| Area | Skills demonstrated |
| --- | --- |
| Files | Create, append, copy, move, compare and mode 700 |
| Text | grep, tr classes, AWK fields, averages and separators |
| Batch | Leading-dash filenames, mode 400, one-argument and NUL-delimited xargs |
| Transfers | Local HTTP GET/PUT, user agent, appended logs and timestamp-aware retrieval |
| Binary | Explicit offsets, octet grouping, training flag and byte round-trip |
| Security design | Assets, trust boundaries, eight risks and proposed controls |

## Folder Structure

```text
cli_lab/           Maintained Python CLI and decimal addition
data/fixtures/     Ten original classroom fixtures
data/manifest.json SHA-256 fixture checksums
data/risk_register.csv  Banking case-study risks
results/demo.json  Checked saved execution
docs/              Report, task guide and references
docs/original/     Original brief and submitted PDF
tools/             Reproducible showcase builder
assets/            Responsive site and shared evidence figures
Makefile           Doctor, demo, test and showcase targets
```

## Setup and Demo

Use Python 3.10+ in Linux or Ubuntu on WSL. Required tools are bash, find, grep, tr, awk, xargs, xxd, curl, wget and stat. From the repository root:

```bash
python3 -m cli_lab doctor
python3 -m cli_lab demo
python3 -m unittest discover -s tests -v
```

From Windows, open this folder in WSL before running the commands. The webpage opens directly from index.html. The Python unit tests also run on Windows from the project root.

### Rebuild the presentation files

Install the document dependencies, then rebuild from the saved JSON evidence:

```bash
python -m pip install -r requirements-docs.txt
python tools/build_showcase.py
```

The builder uses Microsoft Edge on Windows. On Linux, install Chromium with python -m playwright install chromium before building the figures and PDF. The PDF includes the original submission appendix.

## Results

- Saved run: **24/24 exercises passed**.
- Eight AWK records; average **84.875**; highest score **95 (Ayesha)**.
- Five batch-created files verified with owner-read-only mode **400**.
- Sixteen lines reconstructed from the four supplied wordlist parts.
- Loopback upload returned **HTTP 201** and matched its source bytes.
- Local download verified all **37 bytes**; hex round-trip matched its input.

Evidence recorded at 2026-11-18T21:44:56.841506+00:00. See [verification](docs/VERIFICATION.md) for build and browser checks.

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

The evidence format is documented in [Evidence Contract](docs/EVIDENCE_CONTRACT.md). Checks establish consistency with the included fixtures. The JSON file is editable local evidence, so its digest identifies content rather than proving authorship.

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

Start with the [portfolio report](docs/Linux_CLI_Lab_Report.pdf), then inspect a gallery figure and its corresponding JSON step. Run summary to inspect the saved counts, and verify to check the fixture/result relationship. In Linux, run demo for fresh evidence and the regression suite for the failure cases.

The [command guide](docs/TASK_GUIDE.md) maps the maintained demo to all twelve course tasks. [VM administration notes](docs/ADMIN_TASKS.md) cover root, apt and SSH lifecycle operations. The [banking threat model](docs/THREAT_MODEL.md) connects assets, proposed controls and verification ideas.



## Architecture and Responsibilities

The project has four cooperating layers. The command-line entry point selects a task, the execution layer runs real Linux tools, the evidence layer checks saved results, and the presentation builder turns the reviewed evidence into the site, figures and report.

The demo changes files inside a new temporary directory. Original fixtures are read from the repository, checked against their SHA-256 manifest and copied into the workspace. Successful completion writes one JSON result using a temporary file followed by an atomic replacement.

The showcase builder reads the saved result rather than executing commands while a visitor browses the website. This keeps the static GitHub Pages experience usable without a Python service.

| Layer | Maintained file | Responsibility |
| --- | --- | --- |
| Command interface | cli_lab/__main__.py | Parse doctor, demo, verify and summary requests. |
| Execution | cli_lab/lab.py | Check tools, prepare fixtures, execute commands and clean up. |
| Numeric example | cli_lab/addition.py | Parse finite decimal operands and display their sum. |
| Evidence inspection | cli_lab/evidence.py | Validate saved-run structure and fixture-derived outputs. |
| Presentation | tools/build_showcase.py | Rebuild README, webpage, figures and the PDF. |
| Audit | tools/verify_showcase.py | Check navigation order, links, image sizes and the appendix. |

## Reproduction and Platform Guide

Run the command-line project from the repository root with Python 3.10 or newer. Linux, Ubuntu on WSL and the original course VM provide the GNU command environment. On Windows, the saved-evidence commands and Python regression tests can run directly.

doctor checks tool availability and reports whether the Linux execution prerequisites are present. demo executes the full checked sequence. verify inspects an existing JSON result and the current fixtures. summary prints the same verified evidence as a concise category breakdown.

To keep the checked-in evidence while exploring, give demo a different --output path. To inspect that result, provide its path with --evidence. A fresh demo records its own timestamp and durations.

    python3 -m cli_lab doctor
    python3 -m cli_lab demo --output results/my_demo.json
    python3 -m cli_lab verify --evidence results/my_demo.json
    python3 -m cli_lab summary --evidence results/my_demo.json
    python3 -m unittest discover -s tests -v

| Task | Environment | Expected outcome |
| --- | --- | --- |
| Run all 24 exercises | Linux with required GNU tools | Checked JSON evidence in the chosen output path. |
| Inspect a saved run | Python on Windows or Linux | Verified counts, categories and evidence digest. |
| Open the webpage | Browser | Static results, dataset explorer and searchable gallery. |
| Rebuild the showcase | Python, document dependencies and a browser | Shared images, README, site and report. |
| Build targets | GNU Make with Python configured | doctor, demo, test, summary, audit, showcase and verify. |

## Fixture Catalog and Data Interpretation

The ten supplied files total 1,031 bytes. They are small classroom inputs selected to make the result of each command inspectable. The manifest records the expected bytes of every fixture before a demo starts.

The AWK table contains eight rows with four whitespace-separated fields: name, program, city and score. Its scores sum to 679, giving an average of 679 / 8 = 84.875. Ayesha has the highest score, 95. The browser explorer filters these same rows and recalculates the mean for the selected records.

The filename list includes -security_check.txt to exercise operand handling. The four wordlist parts contain sixteen training entries. The account-audit fixture includes a classroom password field; it is demonstration input and should not be used as a real credential.

| Input | Content | Exercises |
| --- | --- | --- |
| awk_task.txt | 8 name/program/city/score records | 12–14; browser data explorer |
| grep_task.txt | Account-audit text and a comment | 06 and 08 |
| xarg_task.txt | 5 filenames, including a leading dash | 15 |
| one/file_list_1.txt; two/file_list_2.txt | Paths to the four supplied parts | 16 |
| parts/shortrockyou_01.txt through 04.txt | 16 classroom wordlist entries | 16 |
| xxd_task.txt | 151-byte inspection sample with a training flag | 22–24 |
| data/manifest.json | SHA-256 expectations for all 10 fixtures | Demo preflight and verify |

## Evidence Lifecycle and Validation

A run records project and schema identifiers, its UTC timestamp, environment information, the passed count and twenty-four ordered steps. Each step includes its command, stdout, stderr, exit code, check result and elapsed milliseconds.

The runner executes commands with a C locale, checks command completion and validates the expected output. Temporary workspace paths are normalized to <workspace> in the saved record. Diagnostic output remains in stderr, including verbose xargs traces.

The evidence inspector checks exercise IDs 01 through 24, required text, successful result fields and finite non-negative timings. It also compares score and wordlist output with the supplied inputs, verifies mode-400 records and checks the recorded transfer length and training flag.

The JSON digest identifies a particular saved file. The record remains editable local evidence. Execution provenance depends on the runner and environment, while the deterministic checks establish consistency with this project.

| Stage | What is checked | Result |
| --- | --- | --- |
| Preflight | Linux tools, fixture paths and SHA-256 values | Invalid or changed inputs stop execution. |
| Command execution | Exit status and explicit output predicate | A failed exercise prevents a successful saved run. |
| Result writing | Complete JSON followed by atomic replacement | Readers see a completed result file. |
| Saved-run inspection | Schema, order, timings and fixture-derived values | Nonzero exit for inconsistent evidence. |
| Presentation audit | Navigation, links, matching images and PDF appendix | A repeatable file-level verification result. |

## Command Workflows and Expected Results

The exercises progress from preparation through files, text pipelines, batching, transfers and binary inspection. Each output is tied to a specific command and assertion. The gallery provides the visible walkthrough, while the JSON preserves the complete command record.

The batch exercise puts -- before filename operands sent to touch and chmod. The separate NUL-delimited example keeps a filename with spaces intact. During reconstruction, xargs -n 1 invokes cat once per supplied part, retaining the classroom list order.

The transfer server binds only to 127.0.0.1 and receives an automatically selected port. curl demonstrates a custom user agent and PUT upload. Wget demonstrates an appended log, an explicit byte-rate cap and timestamp-aware retrieval. The 37-byte fixture checks content correctness rather than sustained network speed.

| Exercise range | Workflow | Checked outcome |
| --- | --- | --- |
| 01–02 | Environment and input discovery | Linux execution and ten fixture paths. |
| 03–05 | File lifecycle, addition and permissions | Matching backup, decimal results and mode 700. |
| 06–11 | find, grep and tr | Scoped fields and expected character transformations. |
| 12–14 | AWK fields and aggregates | 8 score pairs, names, mean 84.875 and top score 95. |
| 15–17 | xargs and filename boundaries | 5 mode-400 files, 16 reconstructed lines and a spaced filename. |
| 18–21 | Loopback HTTP transfers | Verified GET/PUT bytes, HTTP 201 and timestamp-aware fetch. |
| 22–24 | Hex inspection and reconstruction | Offset 0x0a, 3 groups of 3 bytes and exact round-trip. |

## Banking Risk Review and Verification Ideas

The banking case study follows a request across the browser, application, data store, payment integration and operator interfaces. It identifies assets, plausible weaknesses, proposed controls and a way to test those controls in an authorized application environment.

Likelihood and impact use an illustrative 1–5 scale. Priority is their product. The risk register includes eight scenarios; the estimates support a design discussion and require reassessment against a real architecture and operating context.

The local command demo demonstrates handling of files and evidence. It does not implement bank accounts or execute banking security tests. The threat-model document provides the detailed design narrative and the CSV supplies a compact review artifact.

| Scenario | Proposed control | Verification idea |
| --- | --- | --- |
| Account takeover | MFA and secure account recovery | Test recovery and throttling with test identities. |
| Cross-account access | Object-level ownership and role checks | Request another test account's record and require denial. |
| SQL injection | Bound query values and limited database roles | Check that input remains data in the query path. |
| Duplicate transfer | Idempotency and transaction-state validation | Repeat a test request and verify one debit. |
| Session theft | Protected cookies, expiry and rotation | Inspect cookie policy and verify logout/expiry. |
| Sensitive logs | Redaction, access control and retention | Inspect test logs for exposed credentials or account data. |
| Dependency compromise | Inventory, update process and review | Review dependency findings and patch evidence. |
| Service disruption | Capacity, recovery and layered rate controls | Measure behavior in an authorized load exercise. |

## Troubleshooting and Failure Behavior

A failure should point to the layer that needs attention. Start with doctor for tool availability, then inspect the specific exercise or evidence error. Keep the supplied fixtures unchanged while reproducing the saved examples.

A demo failure does not produce a new successful result. The temporary workspace and loopback server are cleaned up through the runner's context and finally handling. A previous saved run can still exist, so inspect recorded_at when distinguishing it from a new execution.

Rebuilding the presentation uses the saved result and shared figure metadata. To change explanatory captions, edit data/showcase.json. To change the additional project documentation, edit data/project_sections.json. Rebuild and verify afterward so the README, site and report agree.

| Symptom | Likely cause | Action |
| --- | --- | --- |
| doctor reports not ready | Windows shell or missing Linux tools | Use Linux/WSL and install the named tool in that environment. |
| Fixture checksum changed | Input bytes were edited or replaced | Compare with the course original before updating the manifest. |
| Exercise fails | Command failed or output differed | Read its reported stdout/stderr and inspect the fixture. |
| Evidence validation fails | Missing step, invalid metadata or inconsistent output | Inspect the JSON and rerun the maintained demo. |
| Showcase browser is unavailable | Browser/runtime prerequisites are missing | Install the documented browser or pass --browser. |
| Older result still displayed | Presentation was built from an earlier saved run | Check recorded_at, rebuild the showcase and refresh. |
| SSH or systemctl reference differs | Distribution or service-manager setup varies | Use the intended VM and inspect its actual unit/service names. |

## Testing Strategy and Review Checklist

The project validates several layers independently. Exercise assertions check real command output, Python regression tests exercise failure cases, and the presentation audit checks the files used by the README, website and report.

The eight regression tests cover finite decimal input, exact small decimal output, invalid numbers, fixture paths, a leading-dash filename, atomic JSON replacement, saved evidence and altered evidence. The tampering test includes a missing step, a changed score, an invalid timing and a failed-result flag.

Browser checks cover the mobile menu, theme switch, all navbar destinations and their active highlight, dataset filtering, gallery search/category behavior, zoom, Previous/Next, keyboard controls, swipe handling and Back to Top. Checks use phone, tablet and desktop widths.

The last twenty-four report pages are compared with the original submission using extracted text, page dimensions and rendered content. A small color-channel tolerance handles merged-document color-profile differences.

| Check layer | Input | Acceptance |
| --- | --- | --- |
| Linux demo | Ten supplied fixtures and loopback server | 24 command/output checks pass. |
| Regression suite | Valid and deliberately inconsistent inputs | 8 tests pass. |
| Evidence audit | Saved JSON and fixture manifest | Ordered valid steps and consistent fixture-derived results. |
| Site and README | Generated links and figure references | All local targets exist and image order matches. |
| Figure export | 24 full images and 24 previews | 1440 × 900 and 960 × 600 pixels. |
| PDF appendix | Original 24-page submission | Text, dimensions and rendered content retained. |
| Responsive controls | 320, 390, 768, 1280 and 1440 px | Both themes and interaction checks pass. |


## Figures

<a id="figure-01"></a>

### 01. Linux environment

[![Linux environment](assets/figures/01-lab-evidence-v2-preview.png)](assets/figures/01-lab-evidence-v2.png)

Confirms the Linux environment before the checked command sequence.

<a id="figure-02"></a>

### 02. Fixture inventory

[![Fixture inventory](assets/figures/02-lab-evidence-v2-preview.png)](assets/figures/02-lab-evidence-v2.png)

Lists all ten supplied fixture files used by the repeatable demo.

<a id="figure-03"></a>

### 03. File lifecycle and backup

[![File lifecycle and backup](assets/figures/03-lab-evidence-v2-preview.png)](assets/figures/03-lab-evidence-v2.png)

Creates an introduction, appends a marker, moves the backup and compares both files.

<a id="figure-04"></a>

### 04. Decimal addition

[![Decimal addition](assets/figures/04-lab-evidence-v2-preview.png)](assets/figures/04-lab-evidence-v2.png)

Adds two decimal values and verifies that 0.1 plus 0.2 is displayed as 0.3.

<a id="figure-05"></a>

### 05. Owner-only executable

[![Owner-only executable](assets/figures/05-lab-evidence-v2-preview.png)](assets/figures/05-lab-evidence-v2.png)

Applies mode 700 to a workspace copy and verifies that the program still runs.

<a id="figure-06"></a>

### 06. Scoped search and account fields

[![Scoped search and account fields](assets/figures/06-lab-evidence-v2-preview.png)](assets/figures/06-lab-evidence-v2.png)

Finds the supplied account-audit file and extracts its username and comment fields.

<a id="figure-07"></a>

### 07. Character class extraction

[![Character class extraction](assets/figures/07-lab-evidence-v2-preview.png)](assets/figures/07-lab-evidence-v2.png)

Uses POSIX digit and hexadecimal classes on controlled input strings.

<a id="figure-08"></a>

### 08. Uppercase conversion

[![Uppercase conversion](assets/figures/08-lab-evidence-v2-preview.png)](assets/figures/08-lab-evidence-v2.png)

Converts the classroom account fixture to uppercase in the C locale.

<a id="figure-09"></a>

### 09. Vowel removal

[![Vowel removal](assets/figures/09-lab-evidence-v2-preview.png)](assets/figures/09-lab-evidence-v2.png)

Removes uppercase and lowercase vowels from a short test phrase.

<a id="figure-10"></a>

### 10. Spaces and repeated characters

[![Spaces and repeated characters](assets/figures/10-lab-evidence-v2-preview.png)](assets/figures/10-lab-evidence-v2.png)

Squeezes repeated spaces and translates the remaining separator into an underscore.

<a id="figure-11"></a>

### 11. Alphanumeric and tab handling

[![Alphanumeric and tab handling](assets/figures/11-lab-evidence-v2-preview.png)](assets/figures/11-lab-evidence-v2.png)

Keeps alphanumeric characters and translates tabs into spaces.

<a id="figure-12"></a>

### 12. AWK name and score columns

[![AWK name and score columns](assets/figures/12-lab-evidence-v2-preview.png)](assets/figures/12-lab-evidence-v2.png)

Reads the first and fourth fields as name:score pairs.

<a id="figure-13"></a>

### 13. Comma-separated names

[![Comma-separated names](assets/figures/13-lab-evidence-v2-preview.png)](assets/figures/13-lab-evidence-v2.png)

Prints all eight student names on one comma-separated line.

<a id="figure-14"></a>

### 14. Score summary

[![Score summary](assets/figures/14-lab-evidence-v2-preview.png)](assets/figures/14-lab-evidence-v2.png)

Calculates the count, average score and highest-scoring record.

<a id="figure-15"></a>

### 15. Batch filenames including a leading dash

[![Batch filenames including a leading dash](assets/figures/15-lab-evidence-v2-preview.png)](assets/figures/15-lab-evidence-v2.png)

Creates five filenames, including a leading-dash name, then verifies mode 400.

<a id="figure-16"></a>

### 16. Rebuild the supplied wordlist

[![Rebuild the supplied wordlist](assets/figures/16-lab-evidence-v2-preview.png)](assets/figures/16-lab-evidence-v2.png)

Reconstructs the 16-line classroom wordlist with one input per invocation.

<a id="figure-17"></a>

### 17. Null-delimited filenames

[![Null-delimited filenames](assets/figures/17-lab-evidence-v2-preview.png)](assets/figures/17-lab-evidence-v2.png)

Preserves a filename containing spaces with NUL-delimited input.

<a id="figure-18"></a>

### 18. Local HTTP request and user agent

[![Local HTTP request and user agent](assets/figures/18-lab-evidence-v2-preview.png)](assets/figures/18-lab-evidence-v2.png)

Fetches a loopback HTTP resource using the requested custom user agent.

<a id="figure-19"></a>

### 19. Local upload and response status

[![Local upload and response status](assets/figures/19-lab-evidence-v2-preview.png)](assets/figures/19-lab-evidence-v2.png)

Uploads to a loopback endpoint, verifies its bytes and checks HTTP 201.

<a id="figure-20"></a>

### 20. Wget log and exact transfer check

[![Wget log and exact transfer check](assets/figures/20-lab-evidence-v2-preview.png)](assets/figures/20-lab-evidence-v2.png)

Downloads a local fixture with an appended log and checks all 37 bytes.

<a id="figure-21"></a>

### 21. Wget timestamp-aware refresh

[![Wget timestamp-aware refresh](assets/figures/21-lab-evidence-v2-preview.png)](assets/figures/21-lab-evidence-v2.png)

Uses timestamp-aware retrieval and verifies the resulting local content.

<a id="figure-22"></a>

### 22. Hex slice from offset 0x0a

[![Hex slice from offset 0x0a](assets/figures/22-lab-evidence-v2-preview.png)](assets/figures/22-lab-evidence-v2.png)

Displays 50 bytes starting at the explicit zero-based offset 0x0a.

<a id="figure-23"></a>

### 23. Three groups of three octets

[![Three groups of three octets](assets/figures/23-lab-evidence-v2-preview.png)](assets/figures/23-lab-evidence-v2.png)

Shows nine bytes per row as three groups of three octets.

<a id="figure-24"></a>

### 24. Flag extraction and byte round-trip

[![Flag extraction and byte round-trip](assets/figures/24-lab-evidence-v2-preview.png)](assets/figures/24-lab-evidence-v2.png)

Extracts the supplied training flag and verifies a byte round-trip.

## Limitations

The saved evidence describes one local Ubuntu/WSL execution. Root access, package installation and SSH service changes are documented VM exercises. The automated demo uses a loopback HTTP server and supplied classroom fixtures. The banking risk scores are conceptual review estimates. A tiny transfer verifies bytes and flags; sustained bandwidth is outside that check.

## About the Author

**Mohammad Rohaan** · BS Computer Science, FAST-NUCES · 22I-2327

- [GitHub profile](https://github.com/rohaan2802)
- [Email](mailto:m.rohaanarshad@gmail.com)

The supplied assignment and original submission remain attributed course artifacts. The maintained code and portfolio evidence are documented separately in the inventory.
