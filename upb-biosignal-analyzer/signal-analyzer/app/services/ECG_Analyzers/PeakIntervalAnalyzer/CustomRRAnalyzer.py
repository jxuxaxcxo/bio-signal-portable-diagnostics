import numpy as np
from scipy.signal import find_peaks
from app.models.ecg_models import ECGInput, ECGSignalFeatures
from app.services.ECG_Analyzers.ecg_feature_extractor import ECGFeatureExtractor


class CustomRRAnalyzer:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.extractor = ECGFeatureExtractor(sample_rate)

    def analyze_ecg_signal(self, input_data: ECGInput):
        features: ECGSignalFeatures = self.extractor.extract_features(input_data)

        # Validación mínima
        num_peaks = len(features.peak_locations) if features.peak_locations else 0
        if num_peaks < 2:
            return False, None, num_peaks

        rr_var = features.rr_variability

        # Consistency check con BPM hint
        if input_data.bpm_hint and features.rr_intervals:
            expected_rr = 60 / input_data.bpm_hint
            deviation_flags = [
                abs(rr - expected_rr) > 0.2 * expected_rr for rr in features.rr_intervals
            ]
            inconsistent_count = sum(deviation_flags)

            if inconsistent_count > len(features.rr_intervals) * 0.3:
                return True, rr_var, num_peaks

        # Default threshold logic
        if rr_var and rr_var > 0.1:
            return True, rr_var, num_peaks

        return False, rr_var, num_peaks
