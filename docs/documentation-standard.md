# Documentation standard

All project documentation, including the root README, follows
[Best practices for GitHub Docs](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs).
These repository conventions apply to authors and documentation agents.

## Writing

- Focus each page on the reader's task or question.
- Put essential information first and procedures in task order.
- Use plain language, active voice, short sentences, and one idea per paragraph.
- Use descriptive headings and links. Add lists, tables, or examples when useful.
- Keep content concise, accessible, and free of unnecessary emphasis.

## Content

- Document current behavior with evidence from source, configuration, or verified results.
- Distinguish configured behavior, successful compilation, automated tests, and hardware validation.
- Do not invent requirements, architecture, features, decisions, or measurements.
- Keep placeholder pages title-only until content is explicitly requested.
- Do not add TODOs, promises of future updates, ownership notes, or work-tracking commentary.
- Keep private instructions and credentials out of public documentation.

## Markdown

- Use GitHub-flavored Markdown and lowercase kebab-case filenames, except established names such as `README.md`.
- Use one level-one title per page, sentence case headings, and consecutive heading levels.
- Separate headings, paragraphs, lists, tables, and code blocks with blank lines.
- Label fenced code blocks with a language; use `text` for plain output.
- Use relative links for repository files. Update indexes and inbound links when moving pages.
- Keep indexes focused on navigation and link to one authoritative page per subject.

## Verification

Run the documentation check from the repository root:

```sh
python scripts/check_docs.py
```

The check covers local file links, headings, and code fences. Review technical
accuracy and rendered readability separately; the check does not validate
external URLs or link anchors.
