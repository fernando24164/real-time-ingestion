from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles validation errors (422) by returning a JSON response with details.
    """
    errors = exc.errors()
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )
