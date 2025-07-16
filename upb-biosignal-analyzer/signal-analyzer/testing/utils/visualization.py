import matplotlib.pyplot as plt
from typing import List

def plot_ecg_sample(
    sample_number: int,
    signal: List[float],
    fs: int,
    detected_afib: bool,
    expected_label: str
):
    """
    Grafica un segmento de señal ECG con información sobre la detección y el label esperado.

    Parámetros:
    - sample_number (int): Sample de inicio (posición en la señal original)
    - signal (List[float]): Lista de valores de la señal
    - fs (int): Frecuencia de muestreo (Hz)
    - detected_afib (bool): Resultado del analizador
    - expected_label (str): Etiqueta real (por ejemplo '(AFIB' o '(N')
    """
    time_axis = [i / fs for i in range(len(signal))]
    
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, signal, label='ECG Signal')
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    
    title = f"Sample {sample_number} | Esperado: {expected_label} | "
    title += "🔴 AFib Detectado" if detected_afib else "🟢 Sin AFib"
    
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
