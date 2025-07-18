from app.models.pcg_models import PCGInput, PCGAnalysisResult
from app.services.PCG_Analyzers.pcg_feature_extractor import PCGFeatureExtractor

class AudioSignalAnalyzer:
    def __init__(self, sample_rate: int = 4000):
        self.sample_rate = sample_rate
        self.feature_extractor = PCGFeatureExtractor(sample_rate)

    def analyze(self, input_data: PCGInput) -> PCGAnalysisResult:
        # Extrae características de la señal
        features = self.feature_extractor.extract_features(input_data.pcg_data)

        # Placeholder: lógica futura para clasificación y soplos
        murmur_detected = self.detect_murmur(features)
        label = "systolic murmur" if murmur_detected else "normal"

        return PCGAnalysisResult(
            heart_sound_peaks=features.s1_peaks + features.s2_peaks,
            bpm=features.bpm,
            murmur_detected=murmur_detected,
            label=label
        )

    def detect_murmur(self, features) -> bool:
        # 🔬 Placeholder: lógica simplificada basada en duración o energía
        if features.bpm and (features.bpm > 130 or features.bpm < 40):
            return True
        if len(features.s1_peaks) < 1 or len(features.s2_peaks) < 1:
            return True
        return False
