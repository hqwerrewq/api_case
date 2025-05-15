from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Auth Service",
    description="Микросервис авторизации",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

from src.api.v1 import auth, users

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")