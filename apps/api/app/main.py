import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import get_settings
from app.routes import explain_router


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    settings = get_settings()
    logging.getLogger(__name__).info(
        "Starting %s %s in %s",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )
    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logging.getLogger(__name__).info("Request validation failed: %s", exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Invalid request payload",
                "code": "VALIDATION_ERROR",
                "errors": jsonable_encoder(exc.errors()),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            detail = exc.detail.get("message", "Request failed")
            code = exc.detail.get("code", "HTTP_ERROR")
        else:
            detail = str(exc.detail)
            code = "HTTP_ERROR"

        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": detail, "code": code},
            headers=exc.headers,
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
        logging.getLogger(__name__).exception("Application validation failed")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal validation error",
                "code": "INTERNAL_VALIDATION_ERROR",
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logging.getLogger(__name__).exception("Unhandled application error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error", "code": "INTERNAL_SERVER_ERROR"},
        )

    app.include_router(explain_router)
    return app


app = create_app()
