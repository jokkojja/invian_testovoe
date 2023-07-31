from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response, JSONResponse
from fastapi import Request

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error occurred", "details": exc.errors()},
    )