from pydantic import BaseModel
from typing import List, Optional

class ECGInput(BaseModel):
    ecg_data: List[float]

class ECGAnalysisResult(BaseModel):
    afib_detected: bool
    bpm: Optional[float] = None
    rr_variability: Optional[float] = None
    num_peaks: Optional[int] = None
