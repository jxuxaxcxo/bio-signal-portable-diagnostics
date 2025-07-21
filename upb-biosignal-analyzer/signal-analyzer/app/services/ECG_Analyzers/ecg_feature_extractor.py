import numpy as np
from scipy.signal import find_peaks
import neurokit2 as nk

from app.models.ecg_models import ECGInput, ECGSignalFeatures


class ECGFeatureExtractor:
    def __init__(self, sample_rate: int = 300):
        self.sample_rate = sample_rate

    def extract_features(self, ecg_input: ECGInput) -> ECGSignalFeatures:
        signal = np.array(ecg_input.ecg_data)
        fs = ecg_input.sample_rate or self.sample_rate

        # Detección simple de R-peaks
        height_threshold = np.max(signal) * 0.1
        distance_threshold = fs / 7  # 7 Hz → 428 ms aprox

        if ecg_input.bpm_hint:
            expected_rr_interval = 60 / ecg_input.bpm_hint
            distance_threshold = expected_rr_interval * fs

        peaks, _ = find_peaks(signal, height=height_threshold, distance=distance_threshold)
        peak_locations = peaks.tolist()

        rr_intervals = np.diff(peaks) / fs
        rr_variability = float(np.var(rr_intervals)) if len(rr_intervals) > 1 else 0.0

        duration_sec = len(signal) / fs
        bpm = len(peaks) * 60 / duration_sec if duration_sec > 0 else None

        return ECGSignalFeatures(
            rr_intervals=rr_intervals.tolist(),
            peak_locations=peak_locations,
            rr_variability=rr_variability,
            bpm=bpm,
            duration_sec=duration_sec,
            # Campos PQRST vacíos en este método
            p_waves=[], q_waves=[], r_peaks=[], s_waves=[], t_waves=[]
        )

    def extract_pqrst_waveforms(self, ecg_input: ECGInput) -> ECGSignalFeatures:
        signal = np.array(ecg_input.ecg_data)
        fs = ecg_input.sample_rate or self.sample_rate

        print("📥 Señal recibida. Largo:", len(signal), " - Frecuencia:", fs)

        try:
            ecg_cleaned = nk.ecg_clean(signal, sampling_rate=fs)
            print("✅ Señal limpiada.")

            # R-peaks desde neurokit2
            rpeaks_output = nk.ecg_peaks(ecg_cleaned, sampling_rate=fs)
            r_peaks = rpeaks_output[1]["ECG_R_Peaks"]
            print("✅ R-peaks detectados:", len(r_peaks))

            delineate = nk.ecg_delineate(ecg_cleaned, rpeaks=r_peaks, sampling_rate=fs, method="peaks")
            print("✅ Delineación completada. Claves disponibles:", delineate[1].keys())

            def clean(peaks):
                if peaks is None:
                    return []
                return [int(p) for p in peaks if not np.isnan(p)]

            # Extra rr_intervals, bpm y variabilidad
            rr_intervals = np.diff(r_peaks) / fs
            rr_variability = float(np.var(rr_intervals)) if len(rr_intervals) > 1 else 0.0
            duration_sec = len(signal) / fs
            bpm = len(r_peaks) * 60 / duration_sec if duration_sec > 0 else None

            return ECGSignalFeatures(
                rr_intervals=rr_intervals.tolist(),
                peak_locations=[],  # Not using scipy peaks here
                rr_variability=rr_variability,
                bpm=bpm,
                duration_sec=duration_sec,
                p_waves=clean(delineate[1].get("ECG_P_Peaks")),
                q_waves=clean(delineate[1].get("ECG_Q_Peaks")),
                r_peaks=r_peaks.tolist(),
                s_waves=clean(delineate[1].get("ECG_S_Peaks")),
                t_waves=clean(delineate[1].get("ECG_T_Peaks"))
            )

        except Exception as e:
            print(f"❌ Error durante extracción de PQRST: {e}")
            return ECGSignalFeatures(
                rr_intervals=[],
                peak_locations=[],
                rr_variability=0.0,
                bpm=None,
                duration_sec=len(signal) / fs,
                p_waves=[], q_waves=[], r_peaks=[], s_waves=[], t_waves=[]
            )
