export type SupportedLanguage =
  | "python"
  | "javascript"
  | "typescript"
  | "java"
  | "c"
  | "cpp"
  | "csharp"
  | "go"
  | "rust"
  | "php"
  | "ruby"
  | "swift"
  | "kotlin"
  | "sql"
  | "shell"
  | "other";

export type ExplainRequest = {
  provider: AIProvider;
  language: SupportedLanguage;
  code: string;
  explanation_language: ExplanationLanguage;
};

export type CodeExplanation = {
  summary: string;
  line_by_line: string;
  functions: string;
  variables: string;
  time_complexity: string;
  space_complexity: string;
  improvements: string;
  beginner_explanation: string;
};

export type ExplainResponse = {
  ok: boolean;
  explanation: CodeExplanation;
  metadata: {
    language: SupportedLanguage;
    model: string;
  };
};

export type ApiErrorResponse = {
  detail: string;
  code: string;
};

export type ExplanationLanguage =
  | "english"
  | "hindi"
  | "telugu";

export type AIProvider =
  | "gemini"
  | "ollama";