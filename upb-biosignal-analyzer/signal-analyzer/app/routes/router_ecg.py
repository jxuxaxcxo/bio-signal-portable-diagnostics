from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional
import numpy as np

from app.models.ecg_models import ECGInput
from app.services.EntropyAnalyzer.EntropyAnalyzer import EntropyAnalyzer
from app.services.PeakIntervalAnalyzer.PeakIntervalAnalyzer import PeakIntervalAnalyzer

router = APIRouter(prefix="/ecg", tags=["ECG"])


@router.get("/health")
def health_check():
    return {"status": "ECG Microservice OK"}


@router.post("/analyze")
async def analyze_ecg(
    data: ECGInput,
    debug: bool = Query(False)
):
    if len(data.ecg_data) == 0:
        raise HTTPException(status_code=400, detail="ECG signal is empty or malformed.")

    # === ANALYZERS ===
    entropy_result = EntropyAnalyzer().analyze_ecg_signal(np.array(data.ecg_data))
    peak_result = PeakIntervalAnalyzer(sample_rate=data.sample_rate or 300).analyze(data)

    if debug:
        print("=== DEBUG: ECG ANALYSIS ===")
        print(f"Entropy Result: {entropy_result}")
        print("PeakInterval Result:", peak_result)
        print("Patient:", data.patient_id)
        print("Recording Time:", data.recording_time)
        print("Time Length:", data.time_lenght)

    return {
        "debug": debug,
        "entropy_analysis": bool(entropy_result),
        "interval_analysis": peak_result
    }
