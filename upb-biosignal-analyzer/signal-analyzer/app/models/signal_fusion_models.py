# app/models/signal_fusion_models.py

from pydantic import BaseModel
from app.models.ecg_models import ECGSignalFeatures
from app.models.pcg_models import PCGSignalFeatures
from typing import Optional


class SignalFusionInput(BaseModel):
    ecg_features: ECGSignalFeatures
    pcg_features: PCGSignalFeatures


class SignalFusionResult(BaseModel):
    correlation_score: float
    diagnostic_suggestion: Optional[str] = None
    notes: Optional[str] = None
