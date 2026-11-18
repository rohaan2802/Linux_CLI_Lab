"""Build the README, static site, 24 evidence figures and the portfolio PDF."""
import argparse
from datetime import datetime
import html
import json
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))
from tools.content_sections import load_sections, markdown_sections, html_section, expand_site, decorate_site
FENCE = chr(96) * 3


def escaped(value):
    return html.escape(str(value))


def table(headers, rows):
    return '<div class="scroll" tabindex="0" role="region" aria-label="' + escaped(headers[0]) + '"><table><thead><tr>' + ''.join('<th scope="col">' + escaped(x) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + str(x) + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def markdown(text):
    lines = text.splitlines()
    output = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("# "):
            output.append("<h1>" + escaped(line[2:]) + "</h1>")
        elif line.startswith("## "):
            output.append("<h2>" + escaped(line[3:]) + "</h2>")
        elif line.startswith("    "):
            code = []
            while index < len(lines) and (lines[index].startswith("    ") or not lines[index].strip()):
                code.append(lines[index][4:])
                index += 1
            output.append("<pre>" + escaped("\n".join(code).rstrip()) + "</pre>")
            continue
        elif line.startswith("- "):
            item = escaped(line[2:])
            item = re.sub(r"(https://[^\s<]+)", r'<a href="\1">\1</a>', item)
            output.append("<p class='list-item'>" + item + "</p>")
        else:
            output.append("<p>" + escaped(line) + "</p>")
        index += 1
    return "\n".join(output)


def icon(paths, css_class=""):
    return f'<svg class="{css_class}" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


def build_texts(settings, demo):
    sections = load_sections(ROOT)
    repository = f"https://github.com/{settings['owner']}/{settings['name']}"
    website = f"https://{settings['owner']}.github.io/{settings['name']}/"
    reference = "https://www.gnu.org/software/coreutils/manual/coreutils.html"
    live = [("Repository", repository), ("GitHub Pages", website), ("GNU command reference", reference)]
    resources = [
        ("Portfolio PDF", "docs/Linux_CLI_Lab_Report.pdf"),
        ("Report source", "docs/Report.md"), ("Evidence contract", "docs/EVIDENCE_CONTRACT.md"), ("Project handbook", "docs/PROJECT_HANDBOOK.md"),
        ("Command guide", "docs/TASK_GUIDE.md"),
        ("CLI source", "cli_lab/lab.py"),
        ("Build file", "Makefile"),
        ("Saved execution", "results/demo.json"),
        ("Threat model", "docs/THREAT_MODEL.md"),
        ("Risk register", "data/risk_register.csv"),
        ("Assignment brief", "docs/original/Assignment_Brief.pdf"),
        ("Original submission", "docs/original/Original_Submission.pdf"),
        ("Original inventory", "docs/INVENTORY.md"),
    ]
    overview = "A repeatable Linux command-line security lab built around CS-3002 coursework. The project runs 24 checked exercises across file operations, permissions, text processing, safe batch filenames, loopback transfers and binary inspection. A banking threat model connects the command-line work with application security."
    methods = "The Python runner verifies fixture checksums, creates a temporary workspace and invokes the real Linux tools with a C locale. Every step has an explicit output check. It closes its local HTTP server and temporary files after completion, then writes JSON evidence atomically."
    boundaries = "The saved evidence describes one local Ubuntu/WSL execution. Root access, package installation and SSH service changes are documented VM exercises. The automated demo uses a loopback HTTP server and supplied classroom fixtures. The banking risk scores are conceptual review estimates. A tiny transfer verifies bytes and flags; sustained bandwidth is outside that check."
    setup = "python3 -m cli_lab doctor\npython3 -m cli_lab demo\npython3 -m unittest discover -s tests -v"
    structure = "cli_lab/           Maintained Python CLI and decimal addition\n data/fixtures/     Ten original classroom fixtures\n data/manifest.json SHA-256 fixture checksums\n data/risk_register.csv  Banking case-study risks\n results/demo.json  Checked saved execution\n docs/              Report, task guide and references\n docs/original/     Original brief and submitted PDF\n tools/             Reproducible showcase builder\n assets/            Responsive site and shared evidence figures\n Makefile           Doctor, demo, test and showcase targets".replace("\n ", "\n")
    captions = []
    by_id = {step["id"]: step for step in demo["steps"]}
    for figure in settings["figures"]:
        step = by_id[figure["id"]]
        captions.append(dict(figure, title=step["title"], category=step["category"],
                             full=f"assets/figures/{figure['slug']}.png",
                             preview=f"assets/figures/{figure['slug']}-preview.png"))

    md = ["<div align=\"center\">", "", "# Linux CLI Lab", "", "**Reproducible Linux fundamentals, command-line evidence and a banking threat model.**", ""]
    badges = [
        ("Python", "python", "cli_lab/lab.py"), ("GNU_Linux", "linux", "docs/TASK_GUIDE.md"),
        ("Bash", "gnubash", "Makefile"), ("Evidence_Audit", "checkmarx", "cli_lab/evidence.py"),
        ("JSON_Results", "json", "results/demo.json"), ("Regression_Tests", "python", "tests/test_lab.py"), ("Rebuildable_Report", "readthedocs", "tools/build_showcase.py"), ("24_Checked_Exercises", "checkmarx", "results/demo.json"),
        ("PDF_Report", "readthedocs", "docs/Linux_CLI_Lab_Report.pdf"),
        ("Security_Case_Study", "owasp", "docs/THREAT_MODEL.md"),
    ]
    md += [f"[![{name}](https://img.shields.io/badge/{name}-145E6B?style=for-the-badge&logo={logo}&logoColor=white)]({target})" for name, logo, target in badges]
    md += ["", "</div>", "", "## Live Links", "", "| What | Link |", "| --- | --- |"]
    md += [f"| {label} | [{url}]({url}) |" for label, url in live]
    md += ["", "## Contents", ""]
    md += [f"- [{name}](#{slug})" for name, slug in [("Overview", "overview"), ("What's Inside", "whats-inside"), ("Project Breakdown", "project-breakdown"), ("Folder Structure", "folder-structure"), ("Setup and Demo", "setup-and-demo"), ("Results", "results"), ("Source and Execution Workflow", "source-and-execution-workflow"), ("Reading the Results", "reading-the-results"), ("Reviewer Walkthrough", "reviewer-walkthrough"), ("Figures", "figures"), ("Limitations", "limitations"), ("About the Author", "about-the-author")]]
    md += [f'- [{section["title"]}](#{re.sub(r"[^a-z0-9]+", "-", section["title"].lower()).strip("-")})' for section in sections]
    md += ["", "## Overview", "", overview, "", "## What's Inside", ""]
    md += [f"- [{title}]({path})" for title, path in resources]
    md += ["", "## Project Breakdown", "", methods, "",
           "| Area | Skills demonstrated |", "| --- | --- |",
           "| Files | Create, append, copy, move, compare and mode 700 |",
           "| Text | grep, tr classes, AWK fields, averages and separators |",
           "| Batch | Leading-dash filenames, mode 400, one-argument and NUL-delimited xargs |",
           "| Transfers | Local HTTP GET/PUT, user agent, appended logs and timestamp-aware retrieval |",
           "| Binary | Explicit offsets, octet grouping, training flag and byte round-trip |",
           "| Security design | Assets, trust boundaries, eight risks and proposed controls |",
           "", "## Folder Structure", "", FENCE+"text", structure, FENCE,
           "", "## Setup and Demo", "",
           "Use Python 3.10+ in Linux or Ubuntu on WSL. Required tools are bash, find, grep, tr, awk, xargs, xxd, curl, wget and stat. From the repository root:", "",
           FENCE+"bash", setup, FENCE, "",
           "From Windows, open this folder in WSL before running the commands. The webpage opens directly from index.html. The Python unit tests also run on Windows from the project root.",
           "", "### Rebuild the presentation files", "",
           "Install the document dependencies, then rebuild from the saved JSON evidence:", "",
           FENCE+"bash", "python -m pip install -r requirements-docs.txt\npython tools/build_showcase.py", FENCE, "",
           "The builder uses Microsoft Edge on Windows. On Linux, install Chromium with python -m playwright install chromium before building the figures and PDF. The PDF includes the original submission appendix.",
           "", "## Results", "",
           f"- Saved run: **{demo['checks_passed']}/24 exercises passed**.",
           "- Eight AWK records; average **84.875**; highest score **95 (Ayesha)**.",
           "- Five batch-created files verified with owner-read-only mode **400**.",
           "- Sixteen lines reconstructed from the four supplied wordlist parts.",
           "- Loopback upload returned **HTTP 201** and matched its source bytes.",
           "- Local download verified all **37 bytes**; hex round-trip matched its input.",
           "", f"Evidence recorded at {demo['recorded_at']}. See [verification](docs/VERIFICATION.md) for build and browser checks.",
           "", "## Figures", ""]
    for figure in captions:
        md += [f"<a id=\"figure-{figure['id']}\"></a>", "", f"### {figure['id']}. {figure['title']}", "",
               f"[![{figure['title']}]({figure['preview']})]({figure['full']})", "", figure["caption"], ""]
    details = (ROOT/"docs/PROJECT_DETAILS.md").read_text(encoding="utf-8")
    details = re.sub(r"\]\(([^):]+)\)", lambda match: "](" + "docs/" + match[1] + ")", details)
    position = md.index("## Figures")
    extended = markdown_sections(sections)
    (ROOT/"docs/PROJECT_HANDBOOK.md").write_text("# Project Handbook\n\n" + extended, encoding="utf-8")
    md[position:position] = [details, "", extended, ""]
    md += ["## Limitations", "", boundaries, "", "## About the Author", "",
           "**Mohammad Rohaan** · BS Computer Science, FAST-NUCES · 22I-2327", "",
           "- [GitHub profile](https://github.com/rohaan2802)",
           "- [Email](mailto:m.rohaanarshad@gmail.com)", "",
           "The supplied assignment and original submission remain attributed course artifacts. The maintained code and portfolio evidence are documented separately in the inventory.", ""]
    (ROOT / "README.md").write_text("\n".join(md), encoding="utf-8")

    nav = [
        ("overview", "Overview"), ("project", "Project"), ("run", "Run"),
        ("results", "Results"), ("explorer", "Data"), ("security", "Security"),
        ("workflow", "Workflow"), ("commands", "Commands"),
        ("gallery", "Gallery"), ("resources", "Files"), ("author", "Author"),
    ]
    menu = icon('<path d="M4 6h16M4 12h16M4 18h16"/>', "hamburger") + icon('<path d="m6 6 12 12M18 6 6 18"/>', "close-icon")
    theme = icon('<path d="M20.7 13.2A9 9 0 0 1 10.8 3.3a9 9 0 1 0 9.9 9.9Z"/>', "moon") + icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>', "sun")
    site = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="description" content="A reproducible Linux command-line security lab with verified outputs and a banking threat model."><title>Linux CLI Lab | Mohammad Rohaan</title><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header><nav class="wrap" aria-label="Main navigation"><a class="brand" href="#overview">Linux CLI Lab</a><button id="menu" class="icon" aria-label="Open menu" aria-expanded="false" aria-controls="nav-links">'+menu+'</button><div id="nav-links">'+''.join(f'<a href="#{key}">{label}</a>' for key,label in nav)+'</div><button id="theme" class="icon" aria-label="Switch theme">'+theme+'</button></nav></header><main id="main">'
    site += '<div class="hero"><div class="wrap"><h1>Linux CLI Lab</h1><p class="lead">Commands you can run. Evidence you can inspect.</p><p>File permissions, text pipelines, batch operations and local transfers, with checked results from 24 repeatable exercises.</p><div class="actions"><a class="action" href="#run">Run the demo</a><a class="action secondary" href="docs/Linux_CLI_Lab_Report.pdf">Read the report</a></div><div class="metrics"><div class="metric"><b>24</b><span>Checked exercises</span></div><div class="metric"><b>10</b><span>Supplied fixture files</span></div><div class="metric"><b>8</b><span>Banking risk scenarios</span></div></div></div></div>'
    site += '<section class="wrap" id="overview"><h2>Overview</h2><p>'+escaped(overview)+'</p><h3>Live Links</h3>'+table(["What","Link"],[(label,f'<a href="{url}">{url}</a>') for label,url in live])+'</section>'
    site += '<section class="wrap" id="project"><h2>What’s inside</h2><p>'+escaped(methods)+'</p><div class="cards"><article class="card"><h3>Maintained source</h3><p>Python command orchestration, finite decimal inputs, fixture validation and atomic result files.</p><a href="cli_lab/lab.py">Inspect the runner</a></article><article class="card"><h3>Reproducible evidence</h3><p>Commands, stdout, exit codes and checks are saved alongside the fixtures and their hashes.</p><a href="results/demo.json">Open the saved run</a></article><article class="card"><h3>Course context</h3><p>Original PDFs, corrected command explanations and a proposed banking control model.</p><a href="docs/TASK_GUIDE.md">Read the task mapping</a></article></div><h3>Folder structure</h3><div class="scroll" role="region" tabindex="0" aria-label="Project folders"><pre>'+escaped(structure)+'</pre></div></section>'
    site += '<section class="wrap" id="run"><h2>Run the project</h2><p>Use Python 3.10+ in Linux or Ubuntu on WSL from the project root. The doctor command checks required tools. The demo creates a temporary local workspace and loopback server.</p><div class="scroll" tabindex="0" role="region" aria-label="Run commands"><pre>'+escaped(setup)+'</pre></div><p>Required tools: bash, find, grep, tr, awk, xargs, xxd, curl, wget and stat. To rebuild the figures and PDF, install requirements-docs.txt and run python tools/build_showcase.py.</p><div class="resource-links"><a class="shortcut" href="Makefile">Makefile</a><a class="shortcut" href="pyproject.toml">Project metadata</a><a class="shortcut" href="cli_lab/__main__.py">CLI entry point</a><a class="shortcut" href="docs/ADMIN_TASKS.md">VM administration guide</a></div></section>'
    stats = [("Checked exercises","24 / 24"),("AWK average","84.875"),("Highest score","Ayesha / 95"),("Wordlist reconstruction","16 lines"),("Batch permissions","400 on five files"),("Upload response","HTTP 201"),("Verified transfer","37 bytes"),("Hex round-trip","Exact match")]
    site += '<section class="wrap" id="results"><h2>Saved results</h2><p>This evidence was recorded at '+escaped(demo["recorded_at"])+'. Each exercise checks its actual command output before the run is saved.</p>'+table(["Measure","Result"],stats)+'<p class="note">'+escaped(boundaries)+'</p></section>'
    students = []
    for line in (ROOT/"data/fixtures/awk_task.txt").read_text().splitlines():
        name, program, city, score = line.split()
        students.append(dict(name=name,program=program,city=city,score=int(score)))
    site += '<section class="wrap" id="explorer"><h2>Explore the AWK dataset</h2><p>Filter the same eight classroom records used by the score summary. The score is the fourth field. The average is recalculated from the selected rows in your browser.</p><label>Minimum score <input id="minimum" type="number" min="0" max="100" value="0" inputmode="numeric"></label><p id="student-summary" role="status"></p><div class="scroll" tabindex="0" role="region" aria-label="Student fixture"><table><thead><tr><th>Name</th><th>Program</th><th>City</th><th>Score</th></tr></thead><tbody id="student-rows"></tbody></table></div><script type="application/json" id="student-data">'+json.dumps(students)+'</script></section>'
    site += '<section class="wrap" id="security"><h2>Banking security case study</h2><p>The original report models an online banking application. The maintained case study maps assets and trust boundaries to eight risks, proposed controls and verification ideas. The scores are illustrative design-review estimates.</p><div class="cards"><article class="card"><h3>Identity and access</h3><p>MFA, secure recovery, session expiry and object-level authorization.</p></article><article class="card"><h3>Transaction integrity</h3><p>Parameterized queries, idempotency and explicit transaction-state checks.</p></article><article class="card"><h3>Operations</h3><p>Redacted logs, dependency review, recovery and capacity planning.</p></article></div><p><a href="docs/THREAT_MODEL.md">Detailed threat model</a> · <a href="data/risk_register.csv" download>Download the risk register</a></p></section>'
    site += '<section class="wrap" id="workflow"><h2>Source and evidence workflow</h2><p>Run the maintained CLI from the repository root. Its verify command checks fixture hashes, exercise structure and fixture-dependent results. summary prints a compact, readable account of the saved run.</p><div class="scroll" tabindex="0" role="region" aria-label="Evidence commands"><pre>python3 -m cli_lab verify\npython3 -m cli_lab summary\npython tools/verify_showcase.py</pre></div><div class="resource-links"><a class="shortcut" href="cli_lab/evidence.py">Evidence validator source</a><a class="shortcut" href="docs/EVIDENCE_CONTRACT.md">Evidence contract</a><a class="shortcut" href="tools/build_showcase.py">PDF and gallery builder</a></div></section>'
    site += '<section class="wrap" id="commands"><h2>Command decisions that matter</h2>'+table(["Goal","Command detail","Reason"],[("Select the score","awk $1 and $4","The score is the fourth field."),("Handle leading dashes","touch -- and chmod 400 --","Filename operands can look like flags."),("Preserve spaces","find -print0 and xargs -0","NUL separates complete filenames."),("State transfer units","wget --limit-rate=125000","A decimal 1 Mbps equals 125000 bytes/s."),("Inspect bytes","xxd -l 50 -s 0x0a","The selected offset is explicit.")])+'<p><a href="docs/TASK_GUIDE.md">Read the complete task mapping</a> for all twelve course tasks, command explanations and VM administration references.</p></section>'
    categories = sorted({f["category"] for f in captions})
    site += '<section class="wrap" id="gallery"><h2>Evidence gallery</h2><p>Each capture contains the executed command and checked output from the saved local run. Open a figure for full resolution.</p><div class="controls"><label>Search figures<input id="gallery-search" type="search" placeholder="Search titles or captions"></label><label>Category<select id="category"><option value="">All categories</option>'+''.join('<option>'+escaped(x)+'</option>' for x in categories)+'</select></label></div><p id="gallery-count" role="status"></p><div class="gallery">'
    for f in captions:
        site += f'<figure data-category="{escaped(f["category"])}"><a href="{f["full"]}"><img src="{f["preview"]}" width="960" height="600" loading="lazy" alt="{escaped(f["title"])}"></a><figcaption><strong>{f["id"]}. {escaped(f["title"])}</strong><span>{escaped(f["caption"])}</span></figcaption></figure>'
    site += '</div></section><section class="wrap" id="resources"><h2>Project files</h2><div class="resource-links">'+''.join(f'<a class="shortcut" href="{path}">{title}</a>' for title,path in resources)+'</div></section>'
    site += '<section class="wrap author" id="author"><h2>About the author</h2><p><strong>Mohammad Rohaan</strong> · BS Computer Science, FAST-NUCES · 22I-2327</p><p><a href="https://github.com/rohaan2802">GitHub profile</a> · <a href="mailto:m.rohaanarshad@gmail.com">Email Mohammad Rohaan</a></p></section></main><footer class="wrap">Linux CLI Lab · Command-line fundamentals and security reasoning</footer>'
    site += '<button id="to-top" aria-label="Back to top" hidden>'+icon('<path fill="currentColor" stroke="none" d="M12 3 2 13h6v8h8v-8h6L12 3Z"/>')+'</button><dialog id="viewer" aria-labelledby="viewer-position"><div class="viewer-controls"><button id="previous">Previous</button><button id="next">Next</button><button id="zoom" aria-pressed="false">Zoom</button><button id="close-viewer">Close</button></div><h3 id="viewer-position"></h3><div class="image-box"><img id="viewer-image" alt=""></div><p id="viewer-caption"></p></dialog></body></html>'
    site = decorate_site(expand_site(site, sections))
    (ROOT/"index.html").write_text(site, encoding="utf-8")
    return captions


def figure_document(step, figure, recorded):
    command = step["command"]
    output = step["stdout"]
    lines = len(output.splitlines())
    size = 48 if lines <= 4 else 38 if lines <= 9 else 29
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
    *{{box-sizing:border-box}}body{{margin:0;width:1440px;height:900px;background:#eaf0f5;color:#233a50;font-family:"Segoe UI",Arial,sans-serif}}
    .frame{{width:1440px;height:900px;padding:27px 30px 20px;border-top:10px solid #5b527a;display:flex;flex-direction:column}}
    .category{{font-size:20px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#535d72}}
    h1{{font-size:47px;line-height:1.1;margin:8px 0 9px;letter-spacing:-1px}}
    .caption{{font-size:25px;line-height:1.3;margin:0 0 16px;color:#44546b}}
    .panels{{display:flex;flex-direction:column;gap:12px;flex:1;min-height:0}}
    .panel{{background:#172c40;color:#fff8df;border-radius:13px;padding:14px 22px;min-width:0;overflow:hidden;display:flex;flex-direction:column}}
    .panel:first-child{{background:#dce5ee;color:#152c43;flex:none}}
    .panel:last-child{{flex:1;min-height:0}}
    .panel h2{{font-size:19px;color:#f3cd82;margin:0 0 9px;text-transform:uppercase;letter-spacing:1px}}
    .panel:first-child h2{{color:#514571}}
    pre{{margin:0;font:28px/1.27 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}}
    .panel:last-child pre{{font-size:{size}px}}
    footer{{margin-top:12px;font-size:19px;color:#4b5d74;display:flex;justify-content:space-between}}
    </style></head><body><div class="frame"><div class="category">{escaped(step["category"])} / checked local execution</div><h1>{escaped(step["title"])}</h1><p class="caption">{escaped(figure["caption"])}</p><div class="panels"><div class="panel"><h2>Executed command</h2><pre>{escaped(command)}</pre></div><div class="panel"><h2>Captured output</h2><pre>{escaped(output)}</pre></div></div><footer><span>Figure {step["id"]} / Linux CLI Lab</span><span>Exit {step["returncode"]} / check passed</span></footer></div></body></html>"""


def make_pdf(page, figures, demo, temporary):
    """Rebuild the report and attach all original submission pages."""
    import pymupdf as fitz
    source = (ROOT/"docs/Report.md").read_text(encoding="utf-8")
    style = """
    @page{size:A4;margin:17mm}*{box-sizing:border-box}body{font:11pt/1.48 "Segoe UI",Arial,sans-serif;color:#213945}
    h1{font-size:29pt;color:#145867;line-height:1.16}h2{font-size:17pt;color:#145867;break-after:avoid}
    p{orphans:3;widows:3}pre{white-space:pre-wrap;font:9.5pt/1.45 Consolas,monospace;padding:12pt;background:#edf2ee}
    table{width:100%;border-collapse:collapse;font-size:9pt;break-inside:avoid}th,td{padding:6pt;border-bottom:.5pt solid #b6c8cb;text-align:left;vertical-align:top;overflow-wrap:anywhere}th{background:#e7f0ed}.project-detail h3{font-size:17pt;color:#145867}.scroll pre{width:auto}.list-item{margin:5pt 0}.chapter{break-before:page}.figure-page{break-before:page}img{width:100%;height:auto;border:1px solid #a4bdc3}
    a{color:#176677;overflow-wrap:anywhere}.caption{color:#445e66}.label{text-transform:uppercase;letter-spacing:2pt;font-size:9pt;color:#627b83}
    """
    chapters = {}
    for chapter in source.split("## ")[1:]:
        title, _, body = chapter.partition("\n")
        chapters[title] = body
    rendered = '<section class="cover"><p class="label">CS-3002 Information Security / Portfolio</p><h1>Linux CLI Lab</h1><h2>Reproducible command-line evidence</h2><p>Mohammad Rohaan / 22I-2327 / FAST-NUCES</p><p>24 checked Linux exercises / 10 original fixtures / banking threat model</p><p>Python orchestration, GNU tools, local transfer verification and documented VM administration.</p><p>Read the command walkthrough, inspect the saved evidence and use the PDF bookmarks to jump between figures. The original 24-page submission is preserved at the end.</p><p>Evidence recorded: '+escaped(demo["recorded_at"])+'</p></section>'
    groups = [
        ["Executive overview","Project contents"],
        ["Reproduction","Corrections and interpretation"],
        ["Execution boundaries","Banking security case study"],
        ["Evidence guide","References","About the author"],
    ]
    for group in groups:
        rendered += '<section class="chapter"><p class="label">Linux CLI Lab / portfolio report</p>'
        for title in group:
            rendered += '<h2>'+escaped(title)+'</h2>'+markdown(chapters[title])
        rendered += '</section>'
    for section in load_sections(ROOT):
        rendered += '<section class="chapter"><p class="label">Project implementation and review</p>' + html_section(section, identifier=False) + "</section>"
    for f in figures:
        step = next(s for s in demo["steps"] if s["id"] == f["id"])
        rendered += '<section class="figure-page"><p class="label">Maintained demo evidence</p><h2>Figure '+f["id"]+' / '+escaped(f["title"])+'</h2><p>'+escaped(f["caption"])+'</p><img src="'+(ROOT/f["full"]).as_uri()+'"><p class="caption">Command exit: 0. Output check: passed. The source commands and output are available in results/demo.json.</p><h2>Read the command</h2><pre>'+escaped(step["command"])+'</pre></section>'
    report_html = temporary/"report.html"
    report_html.write_text('<!doctype html><html><head><meta charset="utf-8"><title>Linux CLI Lab / Portfolio Report</title><style>'+style+'</style></head><body>'+rendered+'</body></html>',encoding="utf-8")
    page.set_viewport_size({"width":794,"height":1123})
    page.goto(report_html.as_uri(), wait_until="load")
    raw = temporary/"report.pdf"
    page.pdf(path=str(raw), print_background=True, prefer_css_page_size=True, display_header_footer=True,
             header_template="<div></div>",
             footer_template='<div style="font:8px Arial;color:#647d86;width:100%;margin:0 64px;display:flex;justify-content:space-between"><span>LINUX CLI LAB / MOHAMMAD ROHAAN</span><span class="pageNumber"></span></div>')
    report = fitz.open(raw)
    original_start = len(report)
    original = fitz.open(ROOT/"docs/original/Original_Submission.pdf")
    report.insert_pdf(original)
    bookmarks = [[1,"Linux CLI Lab",1]]
    detail_titles = [section["title"] for section in load_sections(ROOT)]
    for i, pdf_page in enumerate(report):
        text = pdf_page.get_text()
        if i < original_start:
            for title in ["Executive overview","Project contents","Reproduction","Corrections and interpretation","Execution boundaries","Banking security case study","Evidence guide","References","About the author"]:
                if title in text and not any(x[1]==title for x in bookmarks):
                    bookmarks.append([1,title,i+1])
            for title in detail_titles:
                if title in text and not any(item[1] == title for item in bookmarks):
                    bookmarks.append([1, title, i+1])
            for f in figures:
                if ("Figure "+f["id"]+" /") in text:
                    if f["id"] == "01":
                        bookmarks.append([1,"Maintained demo evidence",i+1])
                    bookmarks.append([2,"Figure "+f["id"]+" / "+f["title"],i+1])
    bookmarks.append([1,"Original submission / 24 pages",original_start+1])
    report.set_toc(bookmarks)
    report.set_metadata({"title":"Linux CLI Lab / Portfolio Report","author":"Mohammad Rohaan","subject":"Linux fundamentals, reproducible command evidence and banking threat model"})
    report.save(ROOT/"docs/Linux_CLI_Lab_Report.pdf", garbage=4, deflate=True)
    print("Portfolio PDF pages:",len(report))
    report.close()
    original.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", default="msedge" if __import__("os").name == "nt" else None)
    args = parser.parse_args()
    settings = json.loads((ROOT/"data/showcase.json").read_text())
    demo = json.loads((ROOT/"results/demo.json").read_text())
    if demo["checks_passed"] != 24 or not all(s["passed"] for s in demo["steps"]):
        raise ValueError("Run the complete checked demo before building the showcase.")
    figures = build_texts(settings,demo)
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory(prefix="cli-showcase-") as folder:
        temporary = Path(folder)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel=args.browser)
            page = browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
            for step, figure in zip(demo["steps"],figures):
                page.set_viewport_size({"width":1440,"height":900})
                page.set_content(figure_document(step,figure,demo["recorded_at"]))
                page.evaluate("""() => {
                  for (const panel of document.querySelectorAll('.panel')) {
                    const pre = panel.querySelector('pre');
                    let size = parseFloat(getComputedStyle(pre).fontSize);
                    while (panel.scrollHeight > panel.clientHeight && size > 20) {
                      size -= .5;
                      pre.style.fontSize = size+'px';
                    }
                    if (panel.scrollHeight > panel.clientHeight) throw new Error('Figure text overflows');
                  }
                }""")
                page.screenshot(path=str(ROOT/figure["full"]),type="png")
                page.add_style_tag(content="body{transform:scale(0.6666666667);transform-origin:0 0}")
                page.set_viewport_size({"width":960,"height":600})
                page.screenshot(path=str(ROOT/figure["preview"]),type="png")
            make_pdf(page,figures,demo,temporary)
            browser.close()
    print("README, webpage and 24 full figures/previews rebuilt.")


if __name__ == "__main__":
    main()
