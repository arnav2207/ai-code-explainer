import asyncio
import json
import logging
import random
from typing import Any

from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.models import CodeExplanation, ExplainRequest, ExplainResponse, ExplanationMetadata
from app.models import AIProvider

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert programming teacher and senior software engineer.
Your job is to explain source code clearly, accurately, and safely.

Rules:
- The JSON property names MUST ALWAYS remain in English.
- Never translate JSON property names.
- Translate ONLY the values.
- The required property names are exactly:
  summary
  line_by_line
  functions
  variables
  time_complexity
  space_complexity
  improvements
  beginner_explanation
- Return ONLY a JSON object. Do not include markdown, code fences, commentary, or prose outside JSON.
- The JSON object must exactly match the requested schema.
- Every value must be a string.
- If a section does not apply, use a short helpful string such as "Not applicable."
- Do not invent behavior that is not present in the code.
- Mention bugs, security risks, edge cases, or unclear behavior when visible from the code.
- Keep explanations beginner-friendly without being vague.
- For line_by_line, explain the code in execution order and reference line numbers when useful.
- For functions, list what each function/method does, or say no functions are defined.
- For variables, explain important variables, parameters, imports, and constants.
- For time_complexity and space_complexity, provide Big-O where it can be inferred, otherwise explain why it depends.
- For improvements, suggest practical code quality, readability, performance, security, or maintainability improvements.
""".strip()

MAX_RETRIES = 3
BASE_RETRY_DELAY_SECONDS = 0.6


class GeminiServiceError(RuntimeError):
    pass


class GeminiInvalidResponseError(GeminiServiceError):
    pass


class GeminiService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def explain_code(self, request: ExplainRequest) -> ExplainResponse:
        prompt = self._build_prompt(request)

        response_text = await self._generate_with_retries(prompt)
        explanation = self._parse_response(response_text)
        return ExplainResponse(
            explanation=explanation,
            metadata=ExplanationMetadata(
                provider=AIProvider.GEMINI,
                language=request.language,
                model=self._settings.gemini_model,
            ),
        )

    async def _generate_with_retries(self, prompt: str) -> str | None:
        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await self._client.aio.models.generate_content(
                    model=self._settings.gemini_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.1,
                        max_output_tokens=4096,
                        response_mime_type="application/json",
                    ),
                )
                return response.text
            except genai_errors.ClientError as exc:
                if self._is_retryable_api_error(exc) and attempt < MAX_RETRIES:
                    last_error = exc
                    await self._sleep_before_retry(attempt)
                    continue

                logger.exception("Gemini client request failed")
                raise GeminiServiceError("The explanation request was rejected by Gemini") from exc
            except (genai_errors.ServerError, genai_errors.APIError) as exc:
                last_error = exc
                if attempt < MAX_RETRIES:
                    logger.warning(
                        "Transient Gemini API failure on attempt %s of %s",
                        attempt,
                        MAX_RETRIES,
                    )
                    await self._sleep_before_retry(attempt)
                    continue

                logger.exception("Gemini API request failed after retries")
                raise GeminiServiceError("The explanation service is temporarily unavailable") from exc
            except Exception as exc:
                logger.exception("Unexpected Gemini service failure")
                raise GeminiServiceError("Failed to generate code explanation") from exc

        logger.exception("Gemini retry loop exhausted", exc_info=last_error)
        raise GeminiServiceError("The explanation service is temporarily unavailable")

    async def _sleep_before_retry(self, attempt: int) -> None:
        delay = BASE_RETRY_DELAY_SECONDS * (2 ** (attempt - 1))
        jitter = random.uniform(0, 0.25)
        await asyncio.sleep(delay + jitter)

    def _is_retryable_api_error(self, exc: genai_errors.APIError) -> bool:
        status_code = getattr(exc, "code", None)
        return status_code in {408, 409, 429, 500, 502, 503, 504}


    def _build_prompt(self, request: ExplainRequest) -> str:
        return f"""
        Explain the following code.

        IMPORTANT:

        Return ALL explanation text in {request.explanation_language.value}.

        The JSON keys MUST remain in English.

        Required JSON keys:

        summary

        line_by_line

        functions

        variables

        time_complexity

        space_complexity

        improvements

        beginner_explanation

        Programming Language:
        {request.language.value}

        Code:

        ```{request.language.value}

        {request.code}"""

    def _parse_response(self, raw_text: str | None) -> CodeExplanation:
        if not raw_text:
            logger.error("Gemini returned an empty response")
            raise GeminiInvalidResponseError("The explanation service returned an empty response")

        try:
            payload: Any = json.loads(raw_text)
            return CodeExplanation.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.exception("Gemini returned an invalid structured response")
            raise GeminiInvalidResponseError("The explanation service returned invalid JSON") from exc
