from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np

from app.services.PeakIntervalAnalyzer.PeakIntervalAnalyzer import PeakIntervalAnalyzer
#from app.services.CrossCorrelationAnalyzer.CrossCorrelationAnalyzer import CorrelationAnalyzer

router = APIRouter(prefix="/correlation", tags=["Correlation"])

@router.post("/linear")
async def correlate_linear(ecg_file: UploadFile = File(...), audio_array_file: UploadFile = File(...), audio_score: str = ""):
    ecg_data = np.fromstring((await ecg_file.read()).decode(), sep=',')
    audio_data = np.fromstring((await audio_array_file.read()).decode(), sep=',')

    if len(ecg_data) == 0 or len(audio_data) == 0:
        raise HTTPException(status_code=400, detail="ECG or audio data is empty")

    bpm = PeakIntervalAnalyzer(sample_rate=300).analyze(ecg_data).get("bpm", None)
    correlation_score = 0  #CorrelationAnalyzer.linear_correlation(ecg_data, audio_data)

    return {
        "bpm_ecg": bpm,
        "audio_score": audio_score,
        "linear_correlation": correlation_score
    }

@router.post("/cross")
async def correlate_cross(ecg_file: UploadFile = File(...), audio_array_file: UploadFile = File(...)):
    ecg_data = np.fromstring((await ecg_file.read()).decode(), sep=',')
    audio_data = np.fromstring((await audio_array_file.read()).decode(), sep=',')

    result = 0 #CorrelationAnalyzer.cross_correlation(ecg_data, audio_data)

    return {
        "correlation_type": "cross",
        "result": result
    }