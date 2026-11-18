"""Shared project detail content for Markdown, the static site and the PDF."""
import html
import json
from pathlib import Path
import re


def load_sections(root):
    return json.loads((Path(root) / "data/project_sections.json").read_text(encoding="utf-8"))


def markdown_sections(sections):
    blocks = []
    for section in sections:
        blocks.extend(["## " + section["title"], ""])
        for paragraph in section["paragraphs"]:
            blocks.extend([paragraph, ""])
        if section.get("code"):
            blocks.extend(["    " + line for line in section["code"].splitlines()])
            blocks.append("")
        blocks.extend([
            "| " + " | ".join(section["headers"]) + " |",
            "| " + " | ".join("---" for _ in section["headers"]) + " |",
        ])
        blocks.extend("| " + " | ".join(row) + " |" for row in section["rows"])
        blocks.append("")
    return "\n".join(blocks)


def html_section(section, identifier=True):
    escape = html.escape
    slug = re.sub(r"[^a-z0-9]+", "-", section["title"].lower()).strip("-")
    attribute = f' id="detail-{slug}"' if identifier else ""
    parts = [f'<article class="project-detail"{attribute}><h3>{escape(section["title"])}</h3>']
    parts.extend("<p>" + escape(text) + "</p>" for text in section["paragraphs"])
    if section.get("code"):
        parts.append('<div class="scroll" tabindex="0" role="region" aria-label="Reproduction commands"><pre>'
                     + escape(section["code"]) + "</pre></div>")
    parts.append('<div class="scroll" tabindex="0" role="region" aria-label="' + escape(section["title"])
                 + '"><table><thead><tr>')
    parts.extend('<th scope="col">' + escape(cell) + "</th>" for cell in section["headers"])
    parts.append("</tr></thead><tbody>")
    for row in section["rows"]:
        parts.append("<tr>" + "".join("<td>" + escape(cell) + "</td>" for cell in row) + "</tr>")
    parts.append("</tbody></table></div></article>")
    return "".join(parts)


def expand_site(site, sections):
    for target in dict.fromkeys(section["target"] for section in sections):
        extra = "".join(html_section(section) for section in sections if section["target"] == target)
        pattern = rf'(<section class="wrap" id="{re.escape(target)}">)(.*?)(</section>)'
        site, count = re.subn(pattern, lambda match: match[1] + match[2] + extra + match[3],
                              site, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f"project detail target is missing: {target}")
    return site
