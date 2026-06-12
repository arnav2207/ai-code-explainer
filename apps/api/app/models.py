from enum import StrEnum
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator


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

class ExplanationLanguage(str, Enum):

    ENGLISH = "english"

    HINDI = "hindi"

    TELUGU = "telugu"


class ExplainRequest(BaseModel):
    language: SupportedLanguage = Field(..., description="Programming language of the submitted code.")
    code: str = Field(..., min_length=1, max_length=30_000, description="Source code to explain.")
    explanation_language: ExplanationLanguage = ExplanationLanguage.ENGLISH

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
    model_config = ConfigDict(extra="forbid")

    summary: str
    line_by_line: str
    functions: str
    variables: str
    time_complexity: str
    space_complexity: str
    improvements: str
    beginner_explanation: str


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
