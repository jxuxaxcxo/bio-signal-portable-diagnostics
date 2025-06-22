import neurokit2 as nk
import numpy as np

class NeurokitAnalyzer:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def analyze_ecg_signal(self, signal, expected_peaks=None):
        try:
            _, info = nk.ecg_process(signal, sampling_rate=self.sample_rate)
            peaks = info.get('ECG_R_Peaks', [])
            num_peaks = len(peaks)

            if num_peaks < 2:
                return False, num_peaks

            rr_intervals = np.diff(peaks) / self.sample_rate
            if rr_intervals.size == 0:
                return False, num_peaks

            rr_var = np.var(rr_intervals)
            afib_detected = rr_var > 0.1
            return afib_detected, num_peaks

        except Exception:
            return False, 0
