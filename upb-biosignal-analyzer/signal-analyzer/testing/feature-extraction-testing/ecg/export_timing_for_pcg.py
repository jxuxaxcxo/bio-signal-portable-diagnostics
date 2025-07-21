import sys
import os
import numpy as np

# 📁 Añadir raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.services.ECG_Analyzers.ecg_feature_extractor import ECGFeatureExtractor
from app.models.ecg_models import ECGInput
from testing.utils.asset_loader import load_sample_ecg_data


def main():
    # ✅ Carga del ECG
    ecg_array, sample_rate = load_sample_ecg_data(
        "04015",             # ID de PhysioNet
        format_hint="wfdb",  # Usar PhysioNet
        max_duration_sec=30  # ⏱️ Máximo 30 segundos
    )

    input_data = ECGInput(ecg_data=ecg_array, sample_rate=sample_rate)
    extractor = ECGFeatureExtractor(sample_rate=sample_rate)
    pqrst = extractor.extract_pqrst_waveforms(input_data)

    print("📊 TIMING INFO for PCG generation:")
    print("Sample rate (Hz):", sample_rate)
    print("Signal length:", len(ecg_array))
    print("Duration (s):", len(ecg_array) / sample_rate)

    def print_list(name, lst):
        print(f"\n{name} ({len(lst)}):")
        print(np.round(np.array(lst) / sample_rate, 3).tolist())  # segundos

    print_list("P wave positions (s)", pqrst["p_waves"])
    print_list("Q wave positions (s)", pqrst["q_waves"])
    print_list("R peaks (s)", pqrst["r_peaks"])
    print_list("S wave positions (s)", pqrst["s_waves"])
    print_list("T wave positions (s)", pqrst["t_waves"])


if __name__ == "__main__":
    main()
