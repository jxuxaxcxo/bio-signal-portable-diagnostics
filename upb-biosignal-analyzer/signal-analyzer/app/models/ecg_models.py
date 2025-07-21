from pydantic import BaseModel
from typing import List, Optional

class ECGInput(BaseModel):
    ecg_data: List[float]  # Señal cruda del ECG
    sample_rate: Optional[int] = 300  # Default: 300 Hz como en tu circuito
    bpm_hint: Optional[float] = None  # Si un análisis externo de audio ya dio un BPM
    audio_label: Optional[str] = None  # Ej: "normal", "systolic murmur", etc.
    patient_id: Optional[str] = None  # Para futuros tests con personas reales
    recording_time: Optional[str] = None  # Para trazabilidad en pruebas reales
    time_lenght: Optional[str] = None

class ECGAnalysisResult(BaseModel):
    afib_detected: bool
    bpm: Optional[float] = None
    rr_variability: Optional[float] = None
    num_peaks: Optional[int] = None

class ECGSignalFeatures(BaseModel):
    rr_intervals: List[float]
    peak_locations: List[int]  # R-peaks
    rr_variability: float
    bpm: Optional[float] = None
    duration_sec: Optional[float] = None

    # Nuevos campos PQRST
    p_waves: List[int] = []
    q_waves: List[int] = []
    r_peaks: List[int] = []  # De Neurokit
    s_waves: List[int] = []
    t_waves: List[int] = []
