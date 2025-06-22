from app.models.ecg_models import ECGInput, ECGAnalysisResult
from app.interfaces.ecg_analyzer_interface import ECGAnalyzerInterface

from .HeartPyAnalyzer import HeartPyAnalyzer
from .NeurokitAnalyzer import NeurokitAnalyzer
from .SimplePeakIntervalAnalyzer import SimplePeakIntervalAnalyzer

import numpy as np
from typing import Optional


class PeakIntervalAnalyzer(ECGAnalyzerInterface):
    def __init__(self, sample_rate: int = 300):
        self.heartpy_analyzer = HeartPyAnalyzer(sample_rate)
        self.neurokit_analyzer = NeurokitAnalyzer(sample_rate)
        self.simple_analyzer = SimplePeakIntervalAnalyzer(sample_rate)

    def analyze(
        self,
        input_data: ECGInput,
        bpm_hint: Optional[float] = None,
        audio_label: Optional[str] = None
    ) -> ECGAnalysisResult:
        signal = np.array(input_data.ecg_data)

        # Run individual analyzers
        heartpy_afib, heartpy_rr_var, heartpy_peaks = self.heartpy_analyzer.analyze(signal)
        neurokit_afib, neurokit_peaks = self.neurokit_analyzer.analyze_ecg_signal(signal)
        simple_afib, simple_rr_var, simple_peaks = self.simple_analyzer.analyze_ecg_signal(signal, bpm_hint)

        # Fusion logic
        fused_afib_suspected = any([heartpy_afib, neurokit_afib, simple_afib])
        if audio_label and "afib" in audio_label.lower():
            fused_afib_suspected = True

        return ECGAnalysisResult(
            afib_detected=fused_afib_suspected,
            bpm=simple_peaks,
            rr_variability=simple_rr_var,
            num_peaks=simple_peaks
        )
