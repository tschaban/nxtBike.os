"""Regression checks for broken documentation links and malformed structure."""

import tempfile
import unittest
from pathlib import Path

from scripts.check_docs import check_document


class DocumentationChecks(unittest.TestCase):
    def check_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target.md").write_text("# Target\n", encoding="utf-8")
            page = root / "README.md"
            page.write_text(text, encoding="utf-8")
            return check_document(page, root)

    def test_relative_links_and_code_examples(self):
        self.assertEqual([], self.check_text(
            "# Example\n\n[Target](target.md#section)\n\n"
            "```text\n[Not a link](missing.md)\n```\n"))

    def test_missing_local_target(self):
        errors = self.check_text("# Example\n\n[Missing](missing.md)\n")
        self.assertTrue(any("missing link target" in error for error in errors))

    def test_invalid_heading_and_unclosed_fence(self):
        errors = self.check_text("# Example\n\n### Skipped\n\n```python\nprint(1)\n")
        self.assertTrue(any("skipped heading" in error for error in errors))
        self.assertTrue(any("unclosed code fence" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
