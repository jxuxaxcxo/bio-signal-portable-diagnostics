import numpy as np
from scipy.signal import find_peaks

class SimplePeakIntervalAnalyzer:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate

    def analyze_ecg_signal(self, signal, bpm_hint=None):
        # Peak detection
        max_height = np.max(signal)
        height_threshold = max_height * 0.1
        distance_threshold = self.sample_rate / 7  # default fallback

        if bpm_hint:
            print("BPM HINT DETECTED")
            print(bpm_hint)
            # Use BPM hint to refine minimum distance between peaks
            expected_rr_interval = 60 / bpm_hint
            distance_threshold = expected_rr_interval * self.sample_rate

        peaks, _ = find_peaks(signal, height=height_threshold, distance=distance_threshold)
        print(f"Detected {len(peaks)} peaks")

        if len(peaks) < 2:
            return False, None, len(peaks)

        rr_intervals = np.diff(peaks) / self.sample_rate
        rr_var = np.var(rr_intervals)

        # Add optional consistency check
        if bpm_hint:
            expected_rr = 60 / bpm_hint
            deviation_flags = [
                abs(rr - expected_rr) > 0.2 * expected_rr for rr in rr_intervals
            ]
            inconsistent_count = sum(deviation_flags)
            print(f"{inconsistent_count}/{len(rr_intervals)} intervals deviate >20% from expected")

            if inconsistent_count > len(rr_intervals) * 0.3:
                print("High deviation from expected RR intervals — possible AFib")
                return True, rr_var, len(peaks)

        # Default threshold logic
        if rr_var > 0.1:
            print("RR variance high — possible AFib")
            return True, rr_var, len(peaks)

        print("RR variability normal — no AFib")
        return False, rr_var, len(peaks)