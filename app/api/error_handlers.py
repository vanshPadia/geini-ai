from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.common.errors import GenieBadException
from fastapi.exceptions import RequestValidationError
from app.configs import log


class ErrorResponse(BaseModel):
    message: str


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(req: Request, ex: RequestValidationError):
        log.error(f'Handle request validation error: {ex.errors()}')
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(message=str(ex)).model_dump()
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(req: Request, ex: ValueError):
        log.error(f"Handle value error: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(message=str(ex)).model_dump()
        )

    @app.exception_handler(GenieBadException)
    async def handle_genie_bad_exception(req: Request, ex: GenieBadException):
        log.error(f"Handle genie bad exception: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(message=ex.message).model_dump()
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(req: Request, ex: HTTPException):
        log.error(f"Handle http exception: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(message=str(ex)).model_dump()
        )

    @app.exception_handler(Exception)
    async def handle_exception(req: Request, ex: Exception):
        log.error(f"Handle exception: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(message=str(ex)).model_dump()
        )
