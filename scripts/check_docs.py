"""Check the public documentation structure and local file links (stdlib only)."""

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


def check_document(path, root):
    errors = []
    fenced = False
    previous_level = 0
    titles = 0
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("```"):
            if not fenced and not line[3:].strip():
                errors.append(f"{path.relative_to(root)}:{number}: code fence needs a language")
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = re.match(r"^(#{1,6}) ", line)
        if heading:
            level = len(heading.group(1))
            titles += level == 1
            if level > previous_level + 1:
                errors.append(f"{path.relative_to(root)}:{number}: skipped heading level")
            previous_level = level
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", line):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            destination = path.parent / unquote(url.path)
            if not destination.exists():
                errors.append(f"{path.relative_to(root)}:{number}: missing link target {target}")
    if titles != 1:
        errors.append(f"{path.relative_to(root)}: expected one level-one title, found {titles}")
    if fenced:
        errors.append(f"{path.relative_to(root)}: unclosed code fence")
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    files = [root / "README.md", root / "CONTRIBUTING.md", *sorted((root / "docs").rglob("*.md"))]
    errors = [error for path in files for error in check_document(path, root)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked {len(files)} documentation files: titles, headings, fences, local file links.")
    print("External URLs, link anchors, rendering, and technical accuracy require separate review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
