import unittest

from aigitgen.cli import _build_parser


class CLITests(unittest.TestCase):
    def test_openai_model_is_default_for_commit(self):
        args = _build_parser().parse_args(["commit"])

        self.assertEqual(args.model, "gpt-5.4")
        self.assertEqual(args.temperature, 0.3)
        self.assertEqual(args.max_tokens, 1024)

    def test_openai_model_can_be_overridden(self):
        args = _build_parser().parse_args(["pr", "--model", "gpt-5.4-mini"])

        self.assertEqual(args.model, "gpt-5.4-mini")


if __name__ == "__main__":
    unittest.main()
