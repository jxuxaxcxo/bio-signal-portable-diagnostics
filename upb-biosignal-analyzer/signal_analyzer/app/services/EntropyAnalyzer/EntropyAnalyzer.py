import neurokit2 as nk
import numpy as np
from scipy.stats import entropy


class EntropyAnalyzer:
    def __init__(self, sample_rate=250, sampen_threshold=0.8, shannon_threshold=1.5, min_window_size=5):
        self.sample_rate = sample_rate
        self.sampen_threshold = sampen_threshold
        self.shannon_threshold = shannon_threshold
        self.min_window_size = min_window_size

    def analyze_ecg_signal(self, signal):
        try:
            print(f"🩺 Starting ECG analysis... Sample rate: {self.sample_rate} Hz")

            # Step 1: Clean ECG
            cleaned_signal = nk.ecg_clean(signal, sampling_rate=self.sample_rate)
            print("✅ ECG signal cleaned.")

            # Step 2: Detect R-peaks
            peaks, _ = nk.ecg_peaks(cleaned_signal, sampling_rate=self.sample_rate)
            r_peaks = np.where(peaks['ECG_R_Peaks'] == 1)[0]
            print(f"📈 R-peaks detected: {len(r_peaks)}")

            if len(r_peaks) < 2:
                return {"error": "Not enough R-peaks detected."}

            # Step 3: Compute RR intervals (in seconds)
            rr_intervals = np.diff(r_peaks) / self.sample_rate
            print(f"🕒 RR intervals (raw): {rr_intervals}")

            if len(rr_intervals) < self.min_window_size:
                return {"error": "Not enough RR intervals for analysis."}

            # Step 4: Normalize RR intervals
            rr_intervals = rr_intervals / np.sum(rr_intervals)
            print(f"🧮 Normalized RR intervals: {rr_intervals}")

            # Step 5: Remove outliers using IQR
            q25, q75 = np.percentile(rr_intervals, [25, 75])
            iqr = q75 - q25
            lower_bound = q25 - 1.5 * iqr
            upper_bound = q75 + 1.5 * iqr
            filtered_rr = rr_intervals[(rr_intervals >= lower_bound) & (rr_intervals <= upper_bound)]
            print(f"🔍 Filtered RR intervals: {filtered_rr}")
            print(f"⚙️ IQR filtering bounds: [{lower_bound}, {upper_bound}]")

            if len(filtered_rr) < self.min_window_size:
                return {"error": "Filtered RR interval window too small."}

            # Step 6: Compute Entropy
            sampen = nk.entropy_sample(filtered_rr)
            shannon = entropy(np.histogram(filtered_rr, bins=10, density=True)[0], base=2)

            # Convert sampen if returned as tuple
            sampen = sampen[0] if isinstance(sampen, tuple) else sampen

            print(f"📊 Sample Entropy (sampen): {sampen}")
            print(f"📊 Shannon Entropy: {shannon}")
            print(f"📏 Thresholds -> sampen: {self.sampen_threshold}, shannon: {self.shannon_threshold}")

            # Step 7: Check for AFib
            detected_afib = bool(sampen > self.sampen_threshold or shannon > self.shannon_threshold)
            print(f"🚨 AFib Detected: {detected_afib}")

            return {
                "sampen": float(sampen),
                "shannon": float(shannon),
                "afib_detected": detected_afib,
                "sampen_threshold": self.sampen_threshold,
                "shannon_threshold": self.shannon_threshold
            }

        except Exception as e:
            print(f"❌ Exception during ECG analysis: {e}")
            return {"error": str(e)}
