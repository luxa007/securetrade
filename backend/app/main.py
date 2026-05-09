from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.api.v1.api import api_router
from app.db.database import Base, engine
from app.middleware.logging_middleware import log_requests
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SecureTrade API",
    description="Scalable REST API with JWT Auth and Role-Based Access",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "SecureTrade API is running", "docs": "/docs"}
