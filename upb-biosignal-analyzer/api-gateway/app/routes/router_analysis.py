from fastapi import APIRouter, Request
from app.services.forwarder import forward_request

router = APIRouter()

@router.post("/ecg")
async def analyze_ecg(request: Request):
    body = await request.json()
    return await forward_request("http://ecg-analysis:5000/analyze", body)

@router.post("/audio")
async def analyze_audio(request: Request):
    body = await request.json()
    return await forward_request("http://audio-analysis:5001/analyze", body)

@router.post("/fusion")
async def analyze_fusion(request: Request):
    body = await request.json()
    return await forward_request("http://fusion-analysis:5002/analyze", body)
