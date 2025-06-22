# app/services/CorrelationAnalyzer.py

import numpy as np
from scipy.signal import correlate
from app.services.utils.signal_helpers import interpolate_to_same_length, normalize_signal


class CorrelationAnalyzer:
    """
    Provides linear and cross-correlation analysis between two signals.
    """

    @staticmethod
    def linear_correlation(signal_a: np.ndarray, signal_b: np.ndarray) -> float:
        """
        Compute Pearson linear correlation between two signals.
        :param signal_a: First signal (ECG)
        :param signal_b: Second signal (e.g., audio-based features)
        :return: Correlation coefficient [-1, 1]
        """
        signal_a, signal_b = interpolate_to_same_length(signal_a, signal_b)
        signal_a = normalize_signal(signal_a)
        signal_b = normalize_signal(signal_b)
        return float(np.corrcoef(signal_a, signal_b)[0, 1])

    @staticmethod
    def cross_correlation(signal_a: np.ndarray, signal_b: np.ndarray) -> dict:
        """
        Compute cross-correlation between two signals.
        :param signal_a: ECG signal
        :param signal_b: Audio signal
        :return: Dict with max correlation and lag
        """
        signal_a, signal_b = interpolate_to_same_length(signal_a, signal_b)
        signal_a = normalize_signal(signal_a)
        signal_b = normalize_signal(signal_b)

        result = correlate(signal_a, signal_b, mode="full")
        lag = int(np.argmax(result) - (len(signal_b) - 1))

        return {
            "max_correlation": float(np.max(result)),
            "lag": lag,
            "correlation_trace": result.tolist()  # Optional: for plotting
        }
