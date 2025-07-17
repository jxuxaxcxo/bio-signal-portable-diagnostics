from app.models.ecg_models import ECGInput, ECGAnalysisResult
from app.interfaces.ecg_analyzer_interface import ECGAnalyzerInterface

from .HeartPyAnalyzer import HeartPyAnalyzer
from .NeurokitAnalyzer import NeurokitAnalyzer
from .CustomRRAnalyzer import CustomRRAnalyzer  # ✅ Nombre actualizado

from typing import Optional


class PeakIntervalAnalyzer(ECGAnalyzerInterface):
    def __init__(self, sample_rate: int = 300):
        self.heartpy_analyzer = HeartPyAnalyzer(sample_rate)
        self.neurokit_analyzer = NeurokitAnalyzer(sample_rate)
        self.custom_rr_analyzer = CustomRRAnalyzer(sample_rate)  # ✅ Renombrado

    def analyze(
        self,
        input_data: ECGInput,
        bpm_hint: Optional[float] = None,
        audio_label: Optional[str] = None
    ) -> ECGAnalysisResult:
        # Run individual analyzers
        heartpy_afib, heartpy_rr_var, heartpy_peaks = self.heartpy_analyzer.analyze(input_data.ecg_data)
        neurokit_afib, neurokit_peaks = self.neurokit_analyzer.analyze_ecg_signal(input_data.ecg_data)
        custom_afib, custom_rr_var, num_custom_peaks = self.custom_rr_analyzer.analyze_ecg_signal(input_data)

        # Fusión de resultados
        fused_afib_suspected = any([heartpy_afib, neurokit_afib, custom_afib])
        if audio_label and "afib" in audio_label.lower():
            fused_afib_suspected = True

        return ECGAnalysisResult(
            afib_detected=fused_afib_suspected,
            bpm=num_custom_peaks,
            rr_variability=custom_rr_var,
            num_peaks=num_custom_peaks
        )

