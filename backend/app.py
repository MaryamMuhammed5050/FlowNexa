from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI(
    title="FlowNexa",
    description="An AI-powered automation platform",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to FlowNexa!",
        "status": "running"
    }