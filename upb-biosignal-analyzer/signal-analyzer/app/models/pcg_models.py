from pydantic import BaseModel
from typing import List, Optional

class PCGInput(BaseModel):
    pcg_data: List[float]  # Señal de audio (PCG) cruda
    sample_rate: Optional[int] = 4000  # Default típico para grabaciones de PCG
    patient_id: Optional[str] = None  # Para trazabilidad clínica
    recording_time: Optional[str] = None  # Fecha/hora de la grabación
    time_length: Optional[str] = None  # Duración en formato legible

class PCGAnalysisResult(BaseModel):
    heart_sound_peaks: Optional[List[float]] = None  # Tiempos (segundos o índices) donde se detectaron S1, S2, etc.
    bpm: Optional[float] = None  # BPM estimado a partir del sonido cardíaco
    murmur_detected: Optional[bool] = None  # Si se detectó algún soplo o anomalía
    label: Optional[str] = None  # Etiqueta general, ej. "normal", "systolic murmur", etc.
