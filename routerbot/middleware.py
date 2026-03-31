import uuid
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    #attach request_id to request state
    request.state.request_id = request_id
    logger.info(
        "[request_id=%s] incoming request: %s %s",
        request_id,
        request.method,
        request.url.path
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "[request_id=%s] response status: %s", 
        request_id, 
        response.status_code 
    )
    return response