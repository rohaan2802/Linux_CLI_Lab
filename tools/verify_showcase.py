"""Verify gallery parity, local links, image dimensions and the original PDF appendix."""
from html.parser import HTMLParser
import json
import html
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class PageLinks(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        for key, value in attributes:
            if key == "id":
                self.ids.append(value)
            if key in ("href", "src") and value:
                self.links.append(value)


def main():
    import pymupdf as fitz
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    markdown = (ROOT / "README.md").read_text(encoding="utf-8")
    page = PageLinks(source)
    assert len(page.ids) == len(set(page.ids)), "duplicate HTML IDs"
    navigation = re.search(r'<div id="nav-links">(.*?)</div>', source, re.S)[1]
    nav_ids = re.findall(r'href="#([^"]+)"', navigation)
    section_ids = re.findall(r'<section[^>]*id="([^"]+)"', source)
    assert nav_ids == section_ids, "navigation order differs from page sections"

    for link in page.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path:
            assert (ROOT / unquote(parsed.path)).is_file(), link
        elif parsed.fragment:
            assert unquote(parsed.fragment) in page.ids, link

    figures = re.findall(r'<figure data-category="([^"]+)"><a href="([^"]+)"><img src="([^"]+)"', source)
    readme = re.findall(r'\[!\[[^\]]+\]\((assets/figures/[^)]+)\)\]\((assets/figures/[^)]+)\)', markdown)
    assert [(preview, full) for _, full, preview in figures] == readme
    assert len(figures) == 24
    for _, full, preview in figures:
        for name, expected in ((full, (1440, 900)), (preview, (960, 600))):
            with (ROOT / name).open("rb") as stream:
                header = stream.read(24)
            assert header[:8] == b"\x89PNG\r\n\x1a\n"
            assert struct.unpack(">II", header[16:24]) == expected, name
    for link in re.findall(r'\]\(([^)]+)\)', markdown):
        if not link.startswith(("#", "https:", "mailto:")):
            assert (ROOT / link).exists(), link
    result = json.loads((ROOT / "results/demo.json").read_text())
    assert result["checks_passed"] == 24
    assert all(step["returncode"] == 0 and step["passed"] for step in result["steps"])
    report = fitz.open(ROOT / "docs/Linux_CLI_Lab_Report.pdf")
    original = fitz.open(ROOT / "docs/original/Original_Submission.pdf")
    handbook = (ROOT / "docs/PROJECT_HANDBOOK.md").read_text(encoding="utf-8")
    report_text = " ".join(" ".join(page.get_text().split()) for page in report)
    for detail in json.loads((ROOT / "data/project_sections.json").read_text(encoding="utf-8")):
        title = detail["title"]
        assert title in markdown and title in handbook, title
        assert html.escape(title) in source, title
        assert title in report_text, title

    assert len(original) == 24
    for i, old_page in enumerate(original):
        new_page = report[len(report) - len(original) + i]
        assert old_page.get_text() == new_page.get_text()
        assert old_page.rect == new_page.rect
        old_pixels = old_page.get_pixmap(matrix=fitz.Matrix(.15, .15)).samples
        new_pixels = new_page.get_pixmap(matrix=fitz.Matrix(.15, .15)).samples
        # Merged document color profiles can shift a channel by a few levels.
        assert len(old_pixels) == len(new_pixels)
        assert max(abs(a - b) for a, b in zip(old_pixels, new_pixels)) <= 5
    print("24 gallery pairs, local paths, PNG sizes, saved checks and all 24 original appendix pages verified.")


if __name__ == "__main__":
    main()
