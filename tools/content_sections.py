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


def decorate_site(site):
    """Add local, accessible SVG symbols without external icon dependencies."""
    import re
    paths = {
        'overview': '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v1"/>',
        'project': '<path d="M3 7h7l2-3h9v16H3Z"/>',
        'run': '<path d="m5 5 7 7-7 7m9 0h6"/>',
        'results': '<path d="M4 20V10m8 10V4m8 16v-7M2 20h20"/>',
        'explorer': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 4 18 4 18 0V5M3 12c0 4 18 4 18 0"/>',
        'security': '<path d="m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6Z"/><path d="m8 12 3 3 5-6"/>',
        'workflow': '<rect x="2" y="3" width="7" height="6" rx="1"/><rect x="15" y="15" width="7" height="6" rx="1"/><path d="M9 6h9v9m-4-4 4 4 4-4"/>',
        'commands': '<path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-16-2 18"/>',
        'gallery': '<rect x="2" y="3" width="20" height="18" rx="2"/><circle cx="8" cy="8" r="2"/><path d="m3 19 6-6 4 4 4-6 5 7"/>',
        'resources': '<path d="M6 2h9l5 5v15H6Z M14 2v6h6M9 12h8m-8 4h8"/>',
        'author': '<circle cx="12" cy="7" r="4"/><path d="M3 22v-3a9 9 0 0 1 18 0v3"/>',
    }
    for key, path in paths.items():
        symbol = '<svg class="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+path+'</svg>'
        pattern = r'(<section[^>]* id="'+key+r'"[^>]*><h2>)([^<]+)(</h2>)'
        site = re.sub(pattern, lambda m: m[1]+symbol+'<span>'+m[2]+'</span>'+m[3], site, count=1)
    return site
