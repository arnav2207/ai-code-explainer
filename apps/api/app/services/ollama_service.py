import json

import httpx

from app.models import (
    CodeExplanation,
    ExplainRequest,
    ExplainResponse,
    ExplanationMetadata,
    AIProvider
)

SYSTEM_PROMPT = """
You are an expert programming teacher and senior software engineer.

Return ONLY valid JSON.

The JSON MUST contain EXACTLY these keys:

{
  "summary": "...",
  "line_by_line": "...",
  "functions": "...",
  "variables": "...",
  "time_complexity": "...",
  "space_complexity": "...",
  "improvements": "...",
  "beginner_explanation": "..."
}

IMPORTANT:
- Every value MUST be a STRING.
- Do NOT return arrays.
- Do NOT return objects.
- Do NOT return markdown.
- Do NOT return code fences.
- Do NOT return explanations outside JSON.
""".strip()


class OllamaService:
    def __init__(self, settings):
        self.settings = settings

    async def explain_code(
        self,
        request: ExplainRequest,
    ) -> ExplainResponse:

        prompt = f"""
Programming Language:
{request.language.value}

Explanation Language:
{request.explanation_language.value}

Code:
{request.code}
"""

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json={
                    "model": self.settings.ollama_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT,
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    "stream": False,
                },
            )
            response.raise_for_status()

        data = response.json()

        try:
            content = data["message"]["content"]
            payload = json.loads(content)
            explanation = CodeExplanation.model_validate(payload)
        except Exception as exc:
            raise RuntimeError(
                "Ollama returned invalid JSON."
            ) from exc

        return ExplainResponse(
            explanation=explanation,
            metadata=ExplanationMetadata(
                provider=AIProvider.OLLAMA,
                language=request.language,
                model=self.settings.ollama_model,
            ),
        )