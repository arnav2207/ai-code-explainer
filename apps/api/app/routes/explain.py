import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.config import get_settings
from app.models import ErrorResponse, ExplainRequest, ExplainResponse
from app.services.ai_factory import AIFactory
from app.services.gemini_service import (
    GeminiInvalidResponseError,
    GeminiServiceError,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["explain"])

@router.post(
    "/explain",
    response_model=ExplainResponse,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
        status.HTTP_502_BAD_GATEWAY: {"model": ErrorResponse},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse},
    },
)
async def explain_code(
    payload: ExplainRequest,
    request: Request,
) -> ExplainResponse:
    logger.info(
        "Received code explanation request",
        extra={
            "language": payload.language.value,
            "code_size": len(payload.code),
            "client": request.client.host if request.client else None,
        },
    )
    settings = get_settings()

    service = AIFactory.create(
        payload.provider,
        settings,
    )

    try:
        return await service.explain_code(payload)
    except GeminiInvalidResponseError as exc:
        logger.warning("Gemini returned an invalid explanation response: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": "INVALID_EXPLANATION_RESPONSE", "message": str(exc)},
        ) from exc
    except GeminiServiceError as exc:
        logger.warning("Code explanation request failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "EXPLANATION_SERVICE_UNAVAILABLE", "message": str(exc)},
        ) from exc
