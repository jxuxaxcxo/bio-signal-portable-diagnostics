from fastapi import APIRouter, Request
from app.services.forwarder import forward_request

router = APIRouter()

@router.post("/ecg")
async def analyze_ecg(request: Request):
    body = await request.json()
    return await forward_request("http://signal_analyzer:8000/ecg/analyze", body)

# Puedes dejar estos para el futuro:
@router.post("/audio")
async def analyze_audio(request: Request):
    body = await request.json()
    return {"message": "Audio analysis temporarily disabled."}

@router.post("/fusion")
async def analyze_fusion(request: Request):
    body = await request.json()
    return {"message": "Fusion analysis temporarily disabled."}
