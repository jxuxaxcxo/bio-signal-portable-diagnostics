import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add root project path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from app.models.ecg_models import ECGInput
from app.models.pcg_models import PCGInput
from app.models.signal_fusion_models import SignalFusionInput, SignalFusionResult
from app.services.ECG_Analyzers.ecg_feature_extractor import ECGFeatureExtractor
from app.services.PCG_Analyzers.pcg_feature_extractor import PCGFeatureExtractor
from app.services.SignalFusion_Analyzers.CrossCorrelationAnalyzer.CrossCorrelationAnalyzer import CrossCorrelationAnalyzer
from testing.utils.asset_loader import load_sample_ecg_data, load_sample_audio_data


def plot_ecg_pcg_overlay(ecg_signal, ecg_sr, pcg_signal, pcg_sr,
                         r_peaks, p_peaks=None, q_points=None, s_points=None, t_peaks=None,
                         s1_peaks=None, s2_peaks=None):
    duration = min(len(ecg_signal)/ecg_sr, len(pcg_signal)/pcg_sr)
    time_ecg = np.linspace(0, duration, len(ecg_signal))
    time_pcg = np.linspace(0, duration, len(pcg_signal))

    plt.figure(figsize=(15, 6))
    plt.plot(time_ecg, ecg_signal, label="ECG", alpha=0.7)
    plt.plot(time_pcg, pcg_signal, label="PCG", alpha=0.6)

    # ECG Markers
    if r_peaks:
        plt.scatter(np.array(r_peaks) / ecg_sr, ecg_signal[r_peaks], color='r', label="R-peaks")
    if p_peaks:
        plt.scatter(np.array(p_peaks) / ecg_sr, ecg_signal[p_peaks], color='g', marker='^', label="P-waves")
    if q_points:
        plt.scatter(np.array(q_points) / ecg_sr, ecg_signal[q_points], color='c', marker='v', label="Q-points")
    if s_points:
        plt.scatter(np.array(s_points) / ecg_sr, ecg_signal[s_points], color='b', marker='s', label="S-points")
    if t_peaks:
        plt.scatter(np.array(t_peaks) / ecg_sr, ecg_signal[t_peaks], color='orange', marker='D', label="T-waves")

    # PCG Markers
    if s1_peaks:
        plt.scatter(np.array(s1_peaks) / pcg_sr, pcg_signal[s1_peaks], color='m', label="S1 (PCG)")
    if s2_peaks:
        plt.scatter(np.array(s2_peaks) / pcg_sr, pcg_signal[s2_peaks], color='k', label="S2 (PCG)")

    plt.xlabel("Time (s)")
    plt.title("ECG and PCG Signals with PQRST and S1/S2 Annotations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    # Carga datos de prueba
    ecg_data, ecg_sr = load_sample_ecg_data("04015", format_hint="wfdb", max_duration_sec=30)
    pcg_data, pcg_sr = load_sample_audio_data("04015.wav")

    # Construye inputs
    ecg_input = ECGInput(ecg_data=ecg_data, sample_rate=ecg_sr)
    pcg_input = PCGInput(pcg_data=pcg_data, sample_rate=pcg_sr)

    # Extrae características
    ecg_features = ECGFeatureExtractor(sample_rate=ecg_sr).extract_pqrst_waveforms(ecg_input)
    pcg_features = PCGFeatureExtractor(sample_rate=pcg_sr).extract_features(pcg_input)

    # Fusiona y analiza
    fusion_input = SignalFusionInput(ecg_features=ecg_features, pcg_features=pcg_features)
    result = CrossCorrelationAnalyzer(sample_rate=pcg_sr).analyze(fusion_input)

    print("📊 Fusion Analysis Result:")
    print(result.model_dump_json(indent=2))

    # Extrae todas las ondas PQRST
    plot_ecg_pcg_overlay(
        ecg_signal=np.array(ecg_input.ecg_data),
        ecg_sr=ecg_sr,
        pcg_signal=np.array(pcg_input.pcg_data),
        pcg_sr=pcg_sr,
        r_peaks=ecg_features.r_peaks or [],
        p_peaks=ecg_features.p_waves or [],
        q_points=ecg_features.q_waves or [],
        s_points=ecg_features.s_waves or [],
        t_peaks=ecg_features.t_waves or [],
        s1_peaks=pcg_features.s1_locations or [],
        s2_peaks=pcg_features.s2_locations or [],
    )


if __name__ == "__main__":
    main()
