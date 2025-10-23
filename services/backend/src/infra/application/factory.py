import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp
from http import HTTPStatus
from typing import Callable, Awaitable
from src.api.rest.v0.routes import api_v0_router
from src.api.rest.v1.routes import api_v1_router
from src.config import AppConfig
from src.infra.application.exception import AppError
from src.infra.application.setup.cors import setup_cors_middleware
from src.infra.application.setup.logging import setup_logging
from src.infra.application.setup.tracing import setup_tracing_middleware

logger = logging.getLogger(__name__)


def create_app_error_handler(app: FastAPI) -> Callable[[Request, Exception], Awaitable[Response]]:
    async def app_error_handler(request: Request, exc: AppError) -> Response:
        logger.warning("Handled AppError: %s", exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"errors": [{"message": exc.detail}]},
        )
    return app_error_handler


def create_internal_exception_handler(app: FastAPI):
    async def internal_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled internal exception: %s", exc)
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={"errors": [{"message": "Internal server error"}]}
        )

    return internal_exception_handler


def app_factory(config: AppConfig) -> ASGIApp:
    setup_logging(config)

    logger.info("starting app")

    app_props = {
        "title": config.app_name,
        "docs_url": config.docs_url,
        "openapi_url": config.openapi_url,
        "redoc_url": None,
    }

    if not config.debug:
        app_props["docs_url"] = None
        app_props["redoc_url"] = None
        app_props["openapi_url"] = None
        logger.info("swagger documentation hidden for security")
    else:
        logger.info(
            "swagger documentation available at %s and %s",
            config.docs_url,
            config.openapi_url,
        )

    app = FastAPI(**app_props)  # type: ignore[arg-type]

    if config.debug:
        logger.info("app started with config")
        masked_config = config.get_config_copy_with_masked_passwords()
        for prop, value in dict(masked_config).items():
            logger.info(" config [%s] has value [%s]", prop, value)

    setup_cors_middleware(app, config)
    setup_tracing_middleware(app, config)

    app.include_router(
        api_v0_router,
        prefix="/api/0",
    )

    # global exception handlers
    app.add_exception_handler(AppError, create_app_error_handler(app))
    app.add_exception_handler(Exception, create_internal_exception_handler(app))

    logger.info("app is ready")

    return app
