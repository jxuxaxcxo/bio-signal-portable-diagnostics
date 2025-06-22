from fastapi import FastAPI
from app.routes.router_ecg import router as ecg_router
from app.routes.router_audio import router as audio_router
from app.routes.router_correlation import router as correlation_router

app = FastAPI()

app.include_router(ecg_router)
app.include_router(audio_router)
app.include_router(correlation_router)
