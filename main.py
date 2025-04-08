from fastapi import FastAPI
from context_understanding.api_router import router as api_router

app = FastAPI(
    title="Email Assistant API",
    description="API for predicting email intent",
    version="1.0.0"
)

app.include_router(api_router)