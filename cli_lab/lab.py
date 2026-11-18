"""Execute isolated Linux exercises and collect checked evidence."""
from datetime import datetime, timezone
from functools import partial
import hashlib
import http.server
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
if not (ROOT / "data/fixtures").is_dir():
    ROOT = Path(sys.prefix) / "share" / "linux-cli-lab"
FIXTURES = ROOT / "data" / "fixtures"
TOOLS = ("bash", "find", "grep", "tr", "awk", "xargs", "xxd", "curl", "wget", "stat")


def doctor():
    return {
        "platform": platform.system(),
        "python": platform.python_version(),
        "tools": {tool: shutil.which(tool) is not None for tool in TOOLS},
        "ready": platform.system() == "Linux" and all(shutil.which(tool) for tool in TOOLS),
    }


def verify_fixtures():
    manifest = json.loads((ROOT / "data/manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest.items():
        path = (FIXTURES / name).resolve()
        if not path.is_relative_to(FIXTURES.resolve()) or not path.is_file():
            raise ValueError(f"fixture is missing or outside the fixture tree: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"fixture checksum changed: {name}")
    return len(manifest)


def validate_fixture_paths(names):
    """Keep the course file lists within the intended fixture tree."""
    resolved = []
    for name in names:
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError(f"invalid fixture path: {name!r}")
        target = (FIXTURES / path).resolve()
        if not target.is_relative_to(FIXTURES.resolve()) or not target.is_file():
            raise ValueError(f"missing or external fixture: {name!r}")
        resolved.append(target)
    return resolved


def atomic_json(destination, value):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".lab-", suffix=".json", dir=destination.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class LocalHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_PUT(self):
        if self.path != "/upload.txt":
            self.send_error(404)
            return
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.server.uploaded = body
        self.send_response(201)
        self.end_headers()
        self.wfile.write(b"upload received\n")


def execute_demo():
    environment = doctor()
    if not environment["ready"]:
        missing = [name for name, ready in environment["tools"].items() if not ready]
        raise RuntimeError("Run in Linux/WSL with these tools available: " + ", ".join(missing or TOOLS))
    verify_fixtures()
    lists = [FIXTURES / "one/file_list_1.txt", FIXTURES / "two/file_list_2.txt"]
    names = [name for path in lists for name in path.read_text().splitlines()]
    validate_fixture_paths(names)
    evidence = []

    with tempfile.TemporaryDirectory(prefix="linux-cli-lab-") as temporary:
        work = Path(temporary)
        shutil.copytree(FIXTURES, work / "input")
        shutil.copy2(Path(__file__).with_name("addition.py"), work / "addition.py")
        (work / "server").mkdir()
        (work / "server/sample.txt").write_bytes(b"Linux CLI Lab local transfer fixture\n")
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(LocalHandler, directory=str(work / "server"))
        )
        server.uploaded = b""
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        port = server.server_address[1]
        env = dict(os.environ, LC_ALL="C", LAB_PORT=str(port), PYTHONDONTWRITEBYTECODE="1")

        def step(identifier, title, category, command, check):
            started = time.monotonic()
            result = subprocess.run(
                ["bash", "-euo", "pipefail", "-c", command],
                cwd=work, env=env, text=True, capture_output=True, timeout=15,
            )
            output = result.stdout.strip()
            if result.returncode or not check(output):
                raise RuntimeError(f"{identifier} failed\n{result.stdout}\n{result.stderr}")
            evidence.append({
                "id": identifier, "title": title, "category": category,
                "command": command, "stdout": output.replace(str(work), "<workspace>"),
                "stderr": result.stderr.strip().replace(str(work), "<workspace>"),
                "returncode": result.returncode, "passed": True,
                "duration_ms": round((time.monotonic() - started) * 1000, 3),
            })

        try:
            step("01", "Linux environment", "Environment",
                 "uname -s\nprintf 'Required command-line tools are available\\n'",
                 lambda out: out.startswith("Linux"))
            step("02", "Fixture inventory", "Environment",
                 "find input -type f | sort",
                 lambda out: len(out.splitlines()) == 10)
            step("03", "File lifecycle and backup", "Files",
                 "mkdir project\nprintf 'Mohammad Rohaan | i222327\\n' > project/introduction.txt\n"
                 "printf 'Project Started\\n' >> project/introduction.txt\n"
                 "cp project/introduction.txt project/backup.txt\nmv project/backup.txt backup.txt\n"
                 "cmp project/introduction.txt backup.txt\ncat backup.txt",
                 lambda out: "Project Started" in out)
            step("04", "Decimal addition", "Files",
                 "python3 addition.py 0.1 0.2", lambda out: out.endswith("0.3"))
            step("05", "Owner-only executable", "Files",
                 "chmod 700 addition.py\nstat -c '%a %A %n' addition.py\npython3 addition.py -4 9.25",
                 lambda out: out.startswith("700 -rwx------") and out.endswith("5.25"))
            step("06", "Scoped search and account fields", "Text",
                 "find input -type f -name grep_task.txt\n"
                 "grep -i -E '^(username|comment):' input/grep_task.txt",
                 lambda out: "areeba.khan" in out and "multi-factor" in out)
            step("07", "Character class extraction", "Text",
                 "printf 'abc42XYZ07\\n' | tr -cd '[:digit:]'\nprintf '\\n'\n"
                 "printf 'G7aQ9Zf\\n' | tr -cd '[:xdigit:]'\nprintf '\\n'",
                 lambda out: out.splitlines() == ["4207", "7a9f"])
            step("08", "Uppercase conversion", "Text",
                 "tr '[:lower:]' '[:upper:]' < input/grep_task.txt",
                 lambda out: "USERNAME: AREEBA.KHAN" in out)
            step("09", "Vowel removal", "Text",
                 "printf 'Information Security\\n' | tr -d 'AEIOUaeiou'",
                 lambda out: out == "nfrmtn Scrty")
            step("10", "Spaces and repeated characters", "Text",
                 "printf 'Linux    lab\\n' | tr -s ' ' | tr ' ' '_'",
                 lambda out: out == "Linux_lab")
            step("11", "Alphanumeric and tab handling", "Text",
                 "printf 'Linux! CLI #2026\\n' | tr -cd '[:alnum:]'\nprintf '\\n'\n"
                 "printf 'name\\tscore\\n' | tr '\\t' ' '",
                 lambda out: out.splitlines() == ["LinuxCLI2026", "name score"])
            step("12", "AWK name and score columns", "Text",
                 "awk '{print $1 \":\" $4}' input/awk_task.txt",
                 lambda out: out.splitlines()[0] == "Ali:78" and len(out.splitlines()) == 8)
            step("13", "Comma-separated names", "Text",
                 "awk 'BEGIN {sep=\"\"} {printf \"%s%s\",sep,$1; sep=\", \"} END {print \"\"}' input/awk_task.txt",
                 lambda out: out == "Ali, Sara, Hamza, Zoya, Usman, Ayesha, Bilal, Hira")
            step("14", "Score summary", "Text",
                 "awk '{sum+=$4; n++; if($4>max){max=$4; top=$1}} "
                 "END {printf \"students=%d average=%.3f top=%s score=%d\\n\",n,sum/n,top,max}' input/awk_task.txt",
                 lambda out: out == "students=8 average=84.875 top=Ayesha score=95")
            step("15", "Batch filenames including a leading dash", "Batch",
                 "mkdir batch\ncd batch\nxargs -a ../input/xarg_task.txt -d '\\n' -t touch --\n"
                 "xargs -a ../input/xarg_task.txt -d '\\n' -t chmod 400 --\n"
                 "find . -type f -printf '%m %f\\n' | sort",
                 lambda out: len(out.splitlines()) == 5 and all(x.startswith("400 ") for x in out.splitlines()))
            step("16", "Rebuild the supplied wordlist", "Batch",
                 "cd input\ncat one/file_list_1.txt two/file_list_2.txt | xargs -n 1 -t cat -- > ../wordlist.txt\n"
                 "cat ../wordlist.txt", lambda out: len(out.splitlines()) == 16 and out.splitlines()[-1] == "cybersecurity")
            step("17", "Null-delimited filenames", "Batch",
                 "mkdir edge\nprintf 'example\\n' > 'edge/file with spaces.txt'\n"
                 "find edge -type f -print0 | xargs -0 -r wc -l --",
                 lambda out: "1 edge/file with spaces.txt" in out)
            step("18", "Local HTTP request and user agent", "Transfer",
                 "curl --fail --silent --show-error --noproxy '*' -A juzztesting "
                 "'http://127.0.0.1:'\"$LAB_PORT\"'/sample.txt'",
                 lambda out: out == "Linux CLI Lab local transfer fixture")
            step("19", "Local upload and response status", "Transfer",
                 "curl --fail --silent --show-error --noproxy '*' -T server/sample.txt "
                 "-w 'HTTP %{http_code}\\n' 'http://127.0.0.1:'\"$LAB_PORT\"'/upload.txt'",
                 lambda out: "HTTP 201" in out)
            if server.uploaded != (work / "server/sample.txt").read_bytes():
                raise RuntimeError("uploaded bytes differ")
            step("20", "Wget log and exact transfer check", "Transfer",
                 "wget --no-proxy --append-output=download.log --limit-rate=125000 --timeout=5 --tries=1 "
                 "-O downloaded.txt 'http://127.0.0.1:'\"$LAB_PORT\"'/sample.txt'\n"
                 "cmp downloaded.txt server/sample.txt\n"
                 "printf 'download bytes verified\\n'\nwc -c < downloaded.txt",
                 lambda out: out == "download bytes verified\n37")
            step("21", "Wget timestamp-aware refresh", "Transfer",
                 "mkdir refresh\ncd refresh\nwget --no-proxy --timestamping --timeout=5 --tries=1 "
                 "'http://127.0.0.1:'\"$LAB_PORT\"'/sample.txt' 2> first.log\n"
                 "wget --no-proxy --timestamping --timeout=5 --tries=1 "
                 "'http://127.0.0.1:'\"$LAB_PORT\"'/sample.txt' 2> second.log\n"
                 "cmp sample.txt ../server/sample.txt\nprintf 'timestamp refresh bytes verified\\n'",
                 lambda out: out == "timestamp refresh bytes verified")
            step("22", "Hex slice from offset 0x0a", "Binary",
                 "xxd -l 50 -s 0x0a input/xxd_task.txt",
                 lambda out: out.startswith("0000000a:"))
            step("23", "Three groups of three octets", "Binary",
                 "xxd -c 9 -g 3 -l 36 input/xxd_task.txt",
                 lambda out: len(out.splitlines()) == 4)
            step("24", "Flag extraction and byte round-trip", "Binary",
                 "grep -o 'flag{[^}]*}' input/xxd_task.txt\n"
                 "xxd -p input/xxd_task.txt | xxd -r -p > restored.txt\n"
                 "cmp restored.txt input/xxd_task.txt\nprintf 'byte round-trip verified\\n'",
                 lambda out: "flag{xxd_offset_master_2026}" in out and "round-trip verified" in out)
        finally:
            server.shutdown()
            server.server_close()
            worker.join()
    return {
        "project": "Linux_CLI_Lab", "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "environment": environment, "checks_passed": len(evidence),
        "scope": "Isolated local Linux workspace and loopback HTTP. Administrative service tasks are documented.",
        "steps": evidence,
    }
