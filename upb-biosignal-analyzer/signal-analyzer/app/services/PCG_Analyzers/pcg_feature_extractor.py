# pcg_feature_extractor.py

import numpy as np
from scipy.signal import find_peaks
from app.models.pcg_models import PCGInput, PCGSignalFeatures


class PCGFeatureExtractor:
    def __init__(self, sample_rate: int = 4000):
        self.sample_rate = sample_rate

    def extract_features(self, input_data: PCGInput) -> PCGSignalFeatures:
        signal = np.array(input_data.pcg_data)
        sr = input_data.sample_rate or self.sample_rate
        duration_sec = len(signal) / sr

        # --- Paso 1: detección general de picos ---
        peak_indices, _ = find_peaks(signal, height=np.max(signal) * 0.2, distance=sr * 0.2)  # cada 200ms

        # --- Paso 2: detección (simplificada) de S1 y S2 ---
        s1_locations = peak_indices[::2].tolist()  # primera mitad de cada ciclo
        s2_locations = peak_indices[1::2].tolist()  # segunda mitad

        # --- Paso 3: intervalos entre S1 (inter-beat) ---
        if len(s1_locations) >= 2:
            inter_beat_intervals = np.diff(s1_locations) / sr
            bpm = 60 / np.mean(inter_beat_intervals)
        else:
            inter_beat_intervals = []
            bpm = None

        # --- Ensamble de resultados ---
        return PCGSignalFeatures(
            inter_beat_intervals=inter_beat_intervals.tolist(),
            peak_locations=peak_indices.tolist(),
            s1_locations=s1_locations,
            s2_locations=s2_locations,
            bpm=bpm,
            duration_sec=duration_sec
        )
