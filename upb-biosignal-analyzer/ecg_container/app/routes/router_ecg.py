from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional
import numpy as np

from app.models.ecg_models import ECGInput
from app.services.EntropyAnalyzer import EntropyAnalyzer
from app.services.PeakIntervalAnalyzer.PeakIntervalAnalyzer import PeakIntervalAnalyzer

router = APIRouter(prefix="/ecg", tags=["ECG"])


@router.get("/health")
def health_check():
    return {"status": "ECG Microservice OK"}


@router.post("/analyze")
async def analyze_ecg(
    file: UploadFile = File(...),
    bpm_hint: Optional[float] = Query(None),
    audio_label: Optional[str] = Query(None),
    debug: bool = Query(False)
):
    try:
        raw_content = await file.read()
        ecg_array = np.fromstring(raw_content.decode(), sep=',')
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ECG file: {str(e)}")

    if len(ecg_array) == 0:
        raise HTTPException(status_code=400, detail="ECG data is empty or malformed.")

    # === ANALYZERS ===
    entropy_result = EntropyAnalyzer().analyze_ecg_signal(ecg_array)
    peak_result = PeakIntervalAnalyzer(sample_rate=300).analyze(ecg_array, bpm_hint=bpm_hint, audio_label=audio_label)

    # === DEBUG PRINTS ===
    if debug:
        print("=== DEBUG: ECG ANALYSIS ===")
        print(f"Entropy Result: {entropy_result}")
        print("PeakInterval Result:")
        print(peak_result)

    return {
        "debug": debug,
        "entropy_analysis": bool(entropy_result),
        "interval_analysis": peak_result
    }
