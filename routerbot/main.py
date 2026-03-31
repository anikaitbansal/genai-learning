import logging
from fastapi import FastAPI
from api_routes import router
from middleware import request_logging_middleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

app = FastAPI(
    title = "GenAI RouterBot API",
    description = " A FastAPI backend for an intent-based GenAI chatbot with memory, routing and reset support.",
    version = "1.0.0"
)

app.middleware("http")(request_logging_middleware)

app.include_router(router)