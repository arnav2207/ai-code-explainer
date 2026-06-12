import json
import logging
from typing import Any

from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import ValidationError

from app.config import Settings
from app.models import CodeExplanation, ExplainRequest, ExplainResponse, ExplanationMetadata

logger = logging.getLogger(__name__)


class GeminiServiceError(RuntimeError):
    pass


class GeminiService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.gemini_api_key)

    async def explain_code(self, request: ExplainRequest) -> ExplainResponse:
        prompt = self._build_prompt(request)

        try:
            response = await self._client.aio.models.generate_content(
                model=self._settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                ),
            )
        except genai_errors.APIError as exc:
            logger.exception("Gemini API request failed")
            raise GeminiServiceError("The explanation service is temporarily unavailable") from exc
        except Exception as exc:
            logger.exception("Unexpected Gemini service failure")
            raise GeminiServiceError("Failed to generate code explanation") from exc

        explanation = self._parse_response(response.text)
        return ExplainResponse(
            explanation=explanation,
            metadata=ExplanationMetadata(
                language=request.language,
                model=self._settings.gemini_model,
            ),
        )

    def _build_prompt(self, request: ExplainRequest) -> str:
        return (
            "You are a senior software engineer explaining code to another developer.\n"
            "Return only valid JSON with this exact shape:\n"
            "{"
            '"summary": string, '
            '"purpose": string, '
            '"key_concepts": string[], '
            '"step_by_step": string[], '
            '"complexity": string | null, '
            '"potential_issues": string[], '
            '"suggested_improvements": string[]'
            "}\n"
            "Keep the explanation accurate, concise, and practical.\n\n"
            f"Language: {request.language.value}\n"
            "Code:\n"
            "```"
            f"{request.language.value}\n"
            f"{request.code}\n"
            "```"
        )

    def _parse_response(self, raw_text: str | None) -> CodeExplanation:
        if not raw_text:
            logger.error("Gemini returned an empty response")
            raise GeminiServiceError("The explanation service returned an empty response")

        try:
            payload: Any = json.loads(raw_text)
            return CodeExplanation.model_validate(payload)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.exception("Gemini returned an invalid structured response")
            raise GeminiServiceError("The explanation service returned invalid JSON") from exc
