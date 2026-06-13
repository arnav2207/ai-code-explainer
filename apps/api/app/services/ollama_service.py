import json

import httpx

from app.models import (
    CodeExplanation,
    ExplainRequest,
    ExplainResponse,
    ExplanationMetadata,
)

SYSTEM_PROMPT = """
You are an expert programming teacher.

Return ONLY valid JSON.

Keys:

summary
line_by_line
functions
variables
time_complexity
space_complexity
improvements
beginner_explanation
""".strip()


class OllamaService:
    def __init__(self, settings):
        self.settings = settings

    async def explain_code(
        self,
        request: ExplainRequest,
    ) -> ExplainResponse:

        prompt = f"""
Language:
{request.language.value}

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

        data = response.json()

        content = data["message"]["content"]

        explanation = CodeExplanation.model_validate(
            json.loads(content)
        )

        return ExplainResponse(
            ok=True,
            explanation=explanation,
            metadata=ExplanationMetadata(
                language=request.language,
                model=self.settings.ollama_model,
            ),
        )