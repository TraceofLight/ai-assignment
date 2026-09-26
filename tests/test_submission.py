"""제출 링크 점검에서 누락을 놓치지 않는지 확인한다."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import run


class SubmissionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in [
            "README.md", "SUBMISSION.md", "src/index.html",
            "docs/CONTRIBUTING.md", "docs/conflict-resolution.md",
            "docs/troubleshooting-log.md", "team/traceoflight.md",
            "team/nansu0425.md", "team/chanpago.md",
        ]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def check(self):
        output = StringIO()
        with patch.object(run, "ROOT", self.root), redirect_stdout(output):
            result = run.main()
        return result, output.getvalue()

    def test_local_html_links_and_external_links_pass(self):
        (self.root / "src/index.html").write_text(
            '<a href="../team/nansu0425.md">소개</a><a href="https://github.com">GitHub</a>',
            encoding="utf-8",
        )
        self.assertEqual(self.check()[0], 0)

    def test_missing_member_fails(self):
        (self.root / "team/chanpago.md").unlink()
        code, output = self.check()
        self.assertEqual(code, 1)
        self.assertIn("누락: team/chanpago.md", output)

    def test_broken_link_in_docs_fails(self):
        (self.root / "docs/CONTRIBUTING.md").write_text(
            "[없는 증빙](../evidence/missing.txt)", encoding="utf-8",
        )
        code, output = self.check()
        self.assertEqual(code, 1)
        self.assertIn("missing.txt", output)
