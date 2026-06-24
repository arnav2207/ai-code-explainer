# AI Code Explainer

Production-ready project.
## Stack

- Frontend: Next.js 15, React, TypeScript, Tailwind CSS, shadcn/ui, Monaco Editor
- Backend: FastAPI, Python 3.12
- LLM: Google Gemini 2.5 Flash using the official `google-genai` SDK, Qwen 2.5B model using Ollama
- Configuration: `.env` with `GEMINI_API_KEY`
- Deployment: Render for backend and Vercel for frontend.

## Current Status

This repository currently contains fully finished project.

## Architecture

The project uses a monorepo layout with separate frontend and backend applications:

- `apps/web` contains the Next.js client application.
- `apps/api` contains the FastAPI service.
- `docs` contains architecture and API documentation.
- `infra` contains deployment and infrastructure configuration.
- `scripts` contains developer automation.

The backend is organized around clean architecture:

- API routes handle HTTP transport.
- Schemas define request and response contracts.
- Domain modules contain entities, ports, and use cases.
- Services integrate external systems such as Gemini.
- Core modules handle configuration, errors, and app-level concerns.

## Environment

Create a local `.env` file from `.env.example` and provide:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```
