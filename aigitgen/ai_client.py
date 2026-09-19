from __future__ import annotations

import os
import time
from dataclasses import dataclass

from openai import APIConnectionError, APIError, APIStatusError, AuthenticationError, OpenAI, RateLimitError

DEFAULT_BASE_URL = "https://copa.codyssey.kr/v1"
DEFAULT_MODEL = "gpt-5.4"


class AIClientError(RuntimeError):
    """Wraps all AI-side failures so the CLI layer can format a single message."""


class MissingAPIKeyError(AIClientError):
    pass


@dataclass
class AIResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


def load_api_key() -> str:
    value = os.environ.get("AI_API_KEY", "").strip()
    if value:
        return value
    raise MissingAPIKeyError(
        "AI_API_KEY 환경변수가 설정되지 않았습니다.\n"
        '  예) Windows PowerShell: $env:AI_API_KEY = "YOUR_KEY"\n'
        '       Bash:               export AI_API_KEY="YOUR_KEY"'
    )


def load_base_url() -> str:
    return os.environ.get("AI_BASE_URL", DEFAULT_BASE_URL).strip() or DEFAULT_BASE_URL


def call_openai(
    system: str,
    user: str,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.3,
    max_tokens: int = 1024,
) -> AIResponse:
    api_key = load_api_key()
    client = OpenAI(api_key=api_key, base_url=load_base_url())
    started = time.monotonic()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except AuthenticationError as exc:
        raise AIClientError("AI API 인증 실패: AI_API_KEY를 확인하세요.") from exc
    except RateLimitError as exc:
        raise AIClientError("AI API 호출이 속도 제한에 걸렸습니다.") from exc
    except APIConnectionError as exc:
        raise AIClientError("AI API 서버에 접속할 수 없습니다. 네트워크 상태를 확인하세요.") from exc
    except APIStatusError as exc:
        raise AIClientError(f"AI API 오류 (status={exc.status_code})") from exc
    except APIError as exc:
        raise AIClientError("AI API 호출에 실패했습니다.") from exc
    except Exception as exc:
        raise AIClientError("AI API 호출 실패") from exc

    elapsed_ms = int((time.monotonic() - started) * 1000)

    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise AIClientError("AI API 응답이 비어 있습니다. max_tokens 를 늘리거나 프롬프트를 점검하세요.")

    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", 0) if usage else 0
    output_tokens = getattr(usage, "completion_tokens", 0) if usage else 0

    return AIResponse(
        text=text,
        model=response.model or model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=elapsed_ms,
    )
