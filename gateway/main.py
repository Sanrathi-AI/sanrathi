"""Standalone dev app for the slides gateway, until it is merged into the
Sanrathi backend. Run from this folder:
    uvicorn main:app --host 127.0.0.1 --port 8100 --env-file .env
"""
from fastapi import FastAPI

import slides_gateway

app = FastAPI(title="Sanrathi gateway (slides)")
app.include_router(slides_gateway.router)
