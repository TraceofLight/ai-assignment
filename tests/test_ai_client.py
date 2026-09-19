import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from aigitgen.ai_client import AIClientError, MissingAPIKeyError, call_openai


class AIClientTests(unittest.TestCase):
    def setUp(self):
        self._old_key = os.environ.get("AI_API_KEY")
        self._old_base_url = os.environ.get("AI_BASE_URL")
        os.environ["AI_API_KEY"] = "test-key"
        os.environ.pop("AI_BASE_URL", None)

    def tearDown(self):
        if self._old_key is None:
            os.environ.pop("AI_API_KEY", None)
        else:
            os.environ["AI_API_KEY"] = self._old_key
        if self._old_base_url is None:
            os.environ.pop("AI_BASE_URL", None)
        else:
            os.environ["AI_BASE_URL"] = self._old_base_url

    @patch("aigitgen.ai_client.OpenAI")
    def test_uses_proxy_default_and_maps_chat_response(self, openai_cls):
        openai_cls.return_value.chat.completions.create.return_value = SimpleNamespace(
            model="gpt-5.4",
            choices=[SimpleNamespace(message=SimpleNamespace(content="generated"))],
            usage=SimpleNamespace(prompt_tokens=12, completion_tokens=7),
        )

        result = call_openai("system", "user", model="gpt-5.4", temperature=0.3, max_tokens=128)

        openai_cls.assert_called_once_with(api_key="test-key", base_url="https://copa.codyssey.kr/v1")
        request = openai_cls.return_value.chat.completions.create.call_args.kwargs
        self.assertEqual(request["model"], "gpt-5.4")
        self.assertEqual(request["messages"], [{"role": "system", "content": "system"}, {"role": "user", "content": "user"}])
        self.assertEqual(request["temperature"], 0.3)
        self.assertEqual(request["max_tokens"], 128)
        self.assertEqual(result.text, "generated")
        self.assertEqual(result.input_tokens, 12)
        self.assertEqual(result.output_tokens, 7)

    @patch("aigitgen.ai_client.OpenAI")
    def test_environment_base_url_overrides_proxy_default(self, openai_cls):
        os.environ["AI_BASE_URL"] = "https://example.test/v1"
        openai_cls.return_value.chat.completions.create.return_value = SimpleNamespace(
            model="custom-model",
            choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))],
            usage=None,
        )

        call_openai("system", "user")

        openai_cls.assert_called_once_with(api_key="test-key", base_url="https://example.test/v1")

    def test_missing_key_raises_without_exposing_secret(self):
        os.environ.pop("AI_API_KEY", None)

        with self.assertRaises(MissingAPIKeyError) as context:
            call_openai("system", "user")

        self.assertNotIn("test-key", str(context.exception))

    @patch("aigitgen.ai_client.OpenAI")
    def test_api_error_is_wrapped_without_exposing_key(self, openai_cls):
        openai_cls.return_value.chat.completions.create.side_effect = RuntimeError("request failed")

        with self.assertRaises(AIClientError) as context:
            call_openai("system", "user")

        self.assertIn("AI API 호출 실패", str(context.exception))
        self.assertNotIn("test-key", str(context.exception))


if __name__ == "__main__":
    unittest.main()
