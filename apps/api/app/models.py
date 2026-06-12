from enum import StrEnum

from pydantic import BaseModel, Field, computed_field, field_validator


class SupportedLanguage(StrEnum):
    python = "python"
    javascript = "javascript"
    typescript = "typescript"
    java = "java"
    c = "c"
    cpp = "cpp"
    csharp = "csharp"
    go = "go"
    rust = "rust"
    php = "php"
    ruby = "ruby"
    swift = "swift"
    kotlin = "kotlin"
    sql = "sql"
    shell = "shell"
    other = "other"


class ExplainRequest(BaseModel):
    language: SupportedLanguage = Field(..., description="Programming language of the submitted code.")
    code: str = Field(..., min_length=1, max_length=30_000, description="Source code to explain.")

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("code must not be empty")
        return normalized


class ExplanationMetadata(BaseModel):
    language: SupportedLanguage
    model: str


class CodeExplanation(BaseModel):
    summary: str = Field(default="")
    purpose: str = Field(default="")
    key_concepts: list[str] = Field(default_factory=list)
    step_by_step: list[str] = Field(default_factory=list)
    complexity: str | None = Field(default=None)
    potential_issues: list[str] = Field(default_factory=list)
    suggested_improvements: list[str] = Field(default_factory=list)


class ExplainResponse(BaseModel):
    explanation: CodeExplanation
    metadata: ExplanationMetadata

    @computed_field
    @property
    def ok(self) -> bool:
        return True


class ErrorResponse(BaseModel):
    detail: str
    code: str
