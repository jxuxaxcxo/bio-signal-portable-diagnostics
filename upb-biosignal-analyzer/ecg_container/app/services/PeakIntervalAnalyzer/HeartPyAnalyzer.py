# HeartPyAnalyzer.py

import heartpy as hp
import numpy as np

class HeartPyAnalyzer:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def analyze(self, signal):
        """
        Detects AFib from an ECG signal using RR interval variability.
        :param signal: ECG signal (list or np.array)
        :return: Tuple (afib_detected: bool, rr_var: float, num_peaks: int)
        """
        try:
            wd, m = hp.process(signal, sample_rate=self.sample_rate)
            peaks = wd['peaklist']
            num_peaks = len(peaks)

            if num_peaks < 2:
                return False, 0.0, num_peaks

            rr_intervals = np.diff(peaks) / self.sample_rate
            if rr_intervals.size == 0:
                return False, 0.0, num_peaks

            rr_var = np.var(rr_intervals)
            afib_detected = rr_var > 0.1  # Example threshold
            return afib_detected, rr_var, num_peaks

        except Exception as e:
            print(f"[HeartPyAnalyzer] Error: {e}")
            return False, 0.0, 0
