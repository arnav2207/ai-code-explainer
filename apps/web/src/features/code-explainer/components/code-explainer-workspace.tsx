"use client";

import { useState } from "react";

import MonacoCodeEditor from "@/components/editor/monaco-code-editor";

import { explainCode } from "@/lib/api";
import type {
  ExplainResponse,
  SupportedLanguage,
} from "@/types/api";

export function CodeExplainerWorkspace() {
  const [language, setLanguage] =
    useState<SupportedLanguage>("python");

  const [code, setCode] = useState(
    `print("Hello, World!")`
  );

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [result, setResult] =
    useState<ExplainResponse | null>(null);

  const handleExplain = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await explainCode({
        language,
        code,
      });

      setResult(response);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unknown error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-8 space-y-6">

      <h1 className="text-3xl font-bold">
        AI Code Explainer
      </h1>

      <select
        value={language}
        onChange={(e) =>
          setLanguage(
            e.target.value as SupportedLanguage
          )
        }
        className="rounded border p-2"
      >
        <option value="python">Python</option>
        <option value="javascript">
          JavaScript
        </option>
        <option value="typescript">
          TypeScript
        </option>
        <option value="java">Java</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="go">Go</option>
        <option value="rust">Rust</option>
      </select>

      <MonacoCodeEditor
        language={language}
        value={code}
        onChange={setCode}
      />

      <button
        onClick={handleExplain}
        disabled={loading}
        className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {loading
          ? "Explaining..."
          : "Explain Code"}
      </button>

      <div className="rounded-lg border p-6">

        <h2 className="mb-4 text-xl font-semibold">
          Explanation
        </h2>

        {error && (
          <div className="mb-4 text-red-500">
            {error}
          </div>
        )}

        {!result && !error && (
          <p className="text-gray-500">
            Explanation will appear here.
          </p>
        )}

        {result && (
          <div className="space-y-6">

            <section>
              <h3 className="font-bold">
                Summary
              </h3>

              <p>
                {result.explanation.summary}
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Line by Line
              </h3>

              <p>
                {
                  result.explanation
                    .line_by_line
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Functions
              </h3>

              <p>
                {
                  result.explanation
                    .functions
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Variables
              </h3>

              <p>
                {
                  result.explanation
                    .variables
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Time Complexity
              </h3>

              <p>
                {
                  result.explanation
                    .time_complexity
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Space Complexity
              </h3>

              <p>
                {
                  result.explanation
                    .space_complexity
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Improvements
              </h3>

              <p>
                {
                  result.explanation
                    .improvements
                }
              </p>
            </section>

            <section>
              <h3 className="font-bold">
                Beginner Explanation
              </h3>

              <p>
                {
                  result.explanation
                    .beginner_explanation
                }
              </p>
            </section>

          </div>
        )}

      </div>

    </div>
  );
}