from pydantic import BaseModel
from typing import List, Optional


class PCGInput(BaseModel):
    pcg_data: List[float]  # Señal de audio (PCG) cruda
    sample_rate: Optional[int] = 4000  # Frecuencia de muestreo típica para PCG
    patient_id: Optional[str] = None  # Para trazabilidad clínica
    recording_time: Optional[str] = None  # Fecha/hora de la grabación
    time_length: Optional[str] = None  # Duración en formato legible


class PCGAnalysisResult(BaseModel):
    heart_sound_peaks: Optional[List[float]] = None  # Tiempos donde se detectaron sonidos cardíacos (S1/S2)
    bpm: Optional[float] = None  # BPM estimado a partir del sonido cardíaco
    murmur_detected: Optional[bool] = None  # Indica si se detectó algún soplo
    label: Optional[str] = None  # Etiqueta general, ej. "normal", "systolic murmur", etc.


class PCGSignalFeatures(BaseModel):
    inter_beat_intervals: List[float]  # Tiempo entre latidos (de un S1 a otro)
    peak_locations: List[int]          # Índices de todos los picos de sonido cardíaco
    s1_locations: List[int]            # Índices específicos de los eventos S1
    s2_locations: List[int]            # Índices específicos de los eventos S2
    bpm: Optional[float] = None
    variability: Optional[float] = None  # ✅ Nueva métrica agregada
    duration_sec: Optional[float] = None
    spectral_entropy: Optional[float] = None  # Extraíble si haces análisis de frecuencia
