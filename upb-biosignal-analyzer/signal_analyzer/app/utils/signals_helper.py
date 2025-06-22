import numpy as np
from scipy.signal import resample


def interpolate_to_same_length(signal_a: np.ndarray, signal_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Trims or interpolates two signals to the same length.
    Uses the shorter length to avoid extrapolation.
    """
    min_len = min(len(signal_a), len(signal_b))
    return signal_a[:min_len], signal_b[:min_len]


def normalize_signal(signal: np.ndarray) -> np.ndarray:
    """
    Scales signal between 0 and 1.
    """
    min_val = np.min(signal)
    max_val = np.max(signal)
    if max_val - min_val == 0:
        return signal  # Avoid division by zero
    return (signal - min_val) / (max_val - min_val)


def smooth_signal(signal: np.ndarray, window_size: int = 5) -> np.ndarray:
    """
    Applies simple moving average to smooth the signal.
    """
    if len(signal) < window_size:
        return signal
    kernel = np.ones(window_size) / window_size
    return np.convolve(signal, kernel, mode='valid')


def resample_signal(signal: np.ndarray, original_rate: int, target_rate: int) -> np.ndarray:
    """
    Resamples the signal to a new sampling rate using interpolation.
    """
    duration = len(signal) / original_rate
    target_length = int(duration * target_rate)
    return resample(signal, target_length)
