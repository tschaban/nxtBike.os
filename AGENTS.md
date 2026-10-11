# Project agent instructions

Read [the documentation index](docs/README.md) and follow
[the documentation standard](docs/documentation-standard.md).
Keep requested documentation placeholders title-only until explicitly asked to
add content. Document current behavior without ownership notes or work-tracking
commentary. Do not treat proposals as accepted decisions.

## Local private configuration

If available, read these installed private instructions before working:

1. `.ai-context/instructions/PROJECT.md`
2. `.ai-context/instructions/WORKFLOW.md`
3. `.ai-context/instructions/DEFINITION_OF_DONE.md`
4. `.ai-context/context/STATUS.md` and `OPEN_QUESTIONS.md` when relevant.

The main session is the developer/coordinator. Delegate to the relevant installed
specialists according to WORKFLOW.md; use independent final review for substantial
changes. Skills live in `.agents/skills/`; custom agents in `.codex/agents/`.
Do not run concurrent firmware builds in this workspace.

These private files are installed from a separate repository and ignored by Git.
Do not publish their contents. The source and revision are recorded in
`.ai-context/installation.json`; edit the source, not installed copies.

## Without private configuration

Public builds and tests must work without it. State that private roles are
unavailable, follow public documentation and user instructions, and label any
self-review honestly. Do not claim a specialist review ran when it did not.

## Verification

- Documentation changes: `python scripts/check_docs.py`.
- Tooling tests: `python -m unittest discover -s tests -v`.
- Firmware/profile changes: use the current environments in
  `config/platformio/environments.ini` and documented profile checks.
- Preserve existing user changes; distinguish compilation from physical-board tests.
