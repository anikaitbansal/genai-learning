from fastapi import FastAPI, HTTPException
from api_routes import router

app = FastAPI()
app.include_router(router)