import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 👇 Añade la raíz del proyecto al path para que funcione la importación desde 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.services.ECG_Analyzers.ecg_feature_extractor import ECGFeatureExtractor
from app.models.ecg_models import ECGInput
from testing.utils.asset_loader import load_sample_ecg_data


def plot_pqrst(signal, sample_rate, r_peaks, p_locs, q_locs, s_locs, t_locs):
    time_axis = np.arange(len(signal)) / sample_rate
    plt.figure(figsize=(14, 5))
    plt.plot(time_axis, signal, label='ECG Signal')

    if len(r_peaks) > 0:
        plt.plot(time_axis[r_peaks], signal[r_peaks], 'ro', label='R-peaks')
    if len(p_locs) > 0:
        plt.plot(time_axis[p_locs], signal[p_locs], 'go', label='P-peaks')
    if len(q_locs) > 0:
        plt.plot(time_axis[q_locs], signal[q_locs], 'co', label='Q-points')
    if len(s_locs) > 0:
        plt.plot(time_axis[s_locs], signal[s_locs], 'mo', label='S-points')
    if len(t_locs) > 0:
        plt.plot(time_axis[t_locs], signal[t_locs], 'yo', label='T-peaks')

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('ECG Signal with PQRST Annotations')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    ecg_array, sample_rate = load_sample_ecg_data(
        "04015",
        format_hint="wfdb",
        max_duration_sec=30
    )

    input_data = ECGInput(ecg_data=ecg_array, sample_rate=sample_rate)
    extractor = ECGFeatureExtractor()
    pqrst_result = extractor.extract_pqrst_waveforms(input_data)

    if not pqrst_result or len(pqrst_result.r_peaks) == 0:
        print("❗ No R-peaks detected. Skipping plot.")
        return

    # ✅ Acceso directo a atributos de ECGSignalFeatures
    r_peaks = np.array(pqrst_result.r_peaks, dtype=int)
    p_peaks = np.array(pqrst_result.p_waves, dtype=int)
    q_points = np.array(pqrst_result.q_waves, dtype=int)
    s_points = np.array(pqrst_result.s_waves, dtype=int)
    t_peaks = np.array(pqrst_result.t_waves, dtype=int)

    print(f"🔍 Detected R: {len(r_peaks)}, P: {len(p_peaks)}, Q: {len(q_points)}, S: {len(s_points)}, T: {len(t_peaks)}")

    plot_pqrst(
        np.array(input_data.ecg_data),
        input_data.sample_rate,
        r_peaks,
        p_peaks,
        q_points,
        s_points,
        t_peaks
    )


if __name__ == "__main__":
    main()
