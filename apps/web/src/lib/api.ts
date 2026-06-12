import { API_BASE_URL } from "@/lib/config";
import type { ApiErrorResponse, ExplainRequest, ExplainResponse } from "@/types/api";

export class ApiClientError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly code?: string,
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

export async function explainCode(payload: ExplainRequest): Promise<ExplainResponse> {
  const response = await fetch(`${API_BASE_URL}/api/explain`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorPayload: Partial<ApiErrorResponse> = {};

    try {
      errorPayload = (await response.json()) as ApiErrorResponse;
    } catch {
      errorPayload = { detail: "Unable to read the error response." };
    }

    throw new ApiClientError(
      errorPayload.detail ?? "The explanation request failed.",
      response.status,
      errorPayload.code,
    );
  }

  return (await response.json()) as ExplainResponse;
}
