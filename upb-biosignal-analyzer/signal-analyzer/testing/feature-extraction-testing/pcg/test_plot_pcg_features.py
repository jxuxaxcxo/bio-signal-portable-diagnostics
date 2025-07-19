# testing/feature-extraction-testing/pcg/test_plot_pcg_features.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from app.services.PCG_Analyzers.pcg_feature_extractor import PCGFeatureExtractor
from app.models.pcg_models import PCGInput

def load_audio(file_path):
    sr, signal = wavfile.read(file_path)

    # Detectar audio estéreo y convertirlo a mono
    print(f"🔍 Shape original de la señal: {signal.shape}")
    if signal.ndim == 2:
        print("⚠️ Audio estéreo detectado. Convirtiendo a mono...")
        signal = signal.mean(axis=1)

    signal = signal.astype(np.float32)
    signal = signal / np.max(np.abs(signal))  # Normalizar
    return signal, sr

def plot_pcg(signal, sr, features):
    time_axis = np.arange(len(signal)) / sr

    plt.figure(figsize=(12, 6))
    plt.plot(time_axis, signal, label="PCG Signal", alpha=0.7)

    # Picos
    plt.plot(np.array(features.peak_locations) / sr, signal[features.peak_locations], 'ro', label="Peaks")

    # S1 y S2
    plt.plot(np.array(features.s1_locations) / sr, signal[features.s1_locations], 'go', label="S1")
    plt.plot(np.array(features.s2_locations) / sr, signal[features.s2_locations], 'mo', label="S2")

    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("PCG Signal with S1, S2, and Peaks")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    file_path = os.path.join(os.path.dirname(__file__), '../../testing-assets/heart-sounds/heart-beat-137135.wav')
    file_path = os.path.abspath(file_path)

    signal, sr = load_audio(file_path)

    print(f"📥 Cargado: {file_path}")
    print(f"🎧 Frecuencia de muestreo: {sr} Hz")
    print(f"🔢 Duración: {len(signal)/sr:.2f} segundos")

    # Extraer características
    extractor = PCGFeatureExtractor(sample_rate=sr)
    input_data = PCGInput(pcg_data=signal.tolist(), sample_rate=sr)
    features = extractor.extract_features(input_data)

    # Imprimir resultados
    print("📊 Resultados del análisis:")
    print(f"   - BPM estimado: {features.bpm}")
    print(f"   - Variabilidad: {features.variability}")
    print(f"   - Duración (s): {features.duration_sec}")

    # Plotear
    plot_pcg(signal, sr, features)

if __name__ == "__main__":
    main()
