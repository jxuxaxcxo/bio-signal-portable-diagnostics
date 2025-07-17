import numpy as np
from scipy.signal import find_peaks

from app.models.ecg_models import ECGInput, ECGSignalFeatures


class ECGFeatureExtractor:
    def __init__(self, sample_rate: int = 300):
        self.sample_rate = sample_rate

    def extract_features(self, ecg_input: ECGInput) -> ECGSignalFeatures:
        signal = np.array(ecg_input.ecg_data)
        fs = ecg_input.sample_rate or self.sample_rate

        # Detectar picos R usando umbral simple (puedes mejorar esto luego)
        height_threshold = np.max(signal) * 0.1
        distance_threshold = fs / 7  # 7 Hz ~ 428 ms

        if ecg_input.bpm_hint:
            expected_rr_interval = 60 / ecg_input.bpm_hint
            distance_threshold = expected_rr_interval * fs

        peaks, _ = find_peaks(signal, height=height_threshold, distance=distance_threshold)
        peak_locations = peaks.tolist()

        # Calcular intervalos RR
        rr_intervals = np.diff(peaks) / fs  # en segundos
        rr_variability = float(np.var(rr_intervals)) if len(rr_intervals) > 1 else 0.0

        # Calcular BPM promedio
        duration_sec = len(signal) / fs
        bpm = len(peaks) * 60 / duration_sec if duration_sec > 0 else None

        return ECGSignalFeatures(
            rr_intervals=rr_intervals.tolist(),
            peak_locations=peak_locations,
            rr_variability=rr_variability,
            bpm=bpm,
            duration_sec=duration_sec
        )
