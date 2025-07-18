import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 👇 Añade la raíz del proyecto al path para que funcione la importación desde 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.services.ECG_Analyzers.ecg_feature_extractor import ECGFeatureExtractor
from app.models.ecg_models import ECGInput
from testing.utils.asset_loader import load_sample_ecg_data  # ✅ Ya existe, solo añadimos función nueva


def plot_r_peaks(signal, sample_rate, r_peaks):
    time_axis = np.arange(len(signal)) / sample_rate
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, signal, label='ECG Signal')
    plt.plot(time_axis[r_peaks], signal[r_peaks], 'ro', label='R-peaks')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('ECG Signal with R-peaks')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    # ✅ Aseguramos que se lea como WFDB (formato PhysioNet)
    ecg_array, sample_rate = load_sample_ecg_data("04908", format_hint="wfdb")

    input_data = ECGInput(ecg_data=ecg_array, sample_rate=sample_rate)
    extractor = ECGFeatureExtractor()
    features = extractor.extract_features(input_data)

    print(f"✅ Detected {len(features.peak_locations)} R-peaks")
    plot_r_peaks(np.array(input_data.ecg_data), input_data.sample_rate, np.array(features.peak_locations))


if __name__ == "__main__":
    main()
