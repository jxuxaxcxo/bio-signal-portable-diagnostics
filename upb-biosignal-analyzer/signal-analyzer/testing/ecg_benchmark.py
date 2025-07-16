import wfdb
import os
import numpy as np

from app.models.ecg_models import ECGInput
from testing.utils.asset_loader import load_assets_codes
from testing.utils.annotation_parser import load_annotations, extract_afib_segments
from testing.utils.visualization import plot_ecg_sample

DEFAULT_FS = 300
SAMPLES_DIR = "testing/testing-assets/mit-bih-arrhythmia-database/"
ASSETS_CODES_PATH = "testing/testing-assets/mit-bih-arrhythmia-database/assetsCodes.json"


def run_single_sample(code: str, analyzer, plot: bool = False, duration_sec: int = 10):
    """
    Corre el analizador sobre un solo sample específico.

    Parámetros:
    - code (str): Código del sample (ej. '08405')
    - analyzer (ECGAnalyzerInterface): Implementación del analizador
    - plot (bool): Si se desea graficar la señal
    - duration_sec (int): Duración del segmento a analizar (por etiqueta)
    """
    record_path = os.path.join(SAMPLES_DIR, code, code)
    annotation = load_annotations(record_path)
    if annotation is None:
        print(f"[ERROR] No se pudo analizar el sample {code} (anotaciones no válidas)")
        return

    segments = extract_afib_segments(annotation)
    if not segments:
        print(f"[INFO] No se encontraron segmentos AFIB ni normales para {code}")
        return

    record = wfdb.rdrecord(record_path)
    fs = record.fs if record.fs else DEFAULT_FS

    matches = 0
    mismatches = 0

    for sample_index, label in segments:
        end = min(sample_index + duration_sec * fs, record.sig_len)
        signal = record.p_signal[sample_index:end, 0].flatten().tolist()

        ecg_input = ECGInput(ecg_data=signal, sample_rate=fs)
        result = analyzer.analyze(ecg_input)

        expected_afib = label == '(AFIB'
        if result.afib_detected == expected_afib:
            matches += 1
        else:
            mismatches += 1

        if plot:
            plot_ecg_sample(
                sample_number=sample_index,
                signal=signal,
                fs=fs,
                detected_afib=result.afib_detected,
                expected_label=label
            )

    print(f"\n[RESULTADO: {code}] Matches: {matches} | Mismatches: {mismatches}")


def run_all_samples(analyzer, plot=False):
    """
    Ejecuta el analizador sobre todos los samples definidos en assetsCodes.json

    Parámetros:
    - analyzer (ECGAnalyzerInterface): Implementación del analizador
    - plot (bool): Si se desea graficar cada sample
    """
    codes = load_assets_codes(ASSETS_CODES_PATH)
    total_matches = 0
    total_mismatches = 0

    for code in codes:
        print(f"\n=== Analizando Sample {code} ===")
        record_path = os.path.join(SAMPLES_DIR, code, code)
        annotation = load_annotations(record_path)
        if annotation is None:
            continue

        record = wfdb.rdrecord(record_path)
        fs = record.fs if record.fs else DEFAULT_FS
        segments = extract_afib_segments(annotation)

        for sample_index, label in segments:
            end = min(sample_index + 10 * fs, record.sig_len)
            signal = record.p_signal[sample_index:end, 0].flatten().tolist()

            ecg_input = ECGInput(ecg_data=signal, sample_rate=fs)
            result = analyzer.analyze(ecg_input)

            expected_afib = label == '(AFIB'
            if result.afib_detected == expected_afib:
                total_matches += 1
            else:
                total_mismatches += 1

            if plot:
                plot_ecg_sample(
                    sample_number=sample_index,
                    signal=signal,
                    fs=fs,
                    detected_afib=result.afib_detected,
                    expected_label=label
                )

    print("\n📊 RESULTADOS TOTALES")
    print(f"✔ Matches: {total_matches}")
    print(f"✖ Mismatches: {total_mismatches}")
    accuracy = 100 * total_matches / (total_matches + total_mismatches)
    print(f"🎯 Precisión total: {accuracy:.2f}%")


def run_with_custom_analyzer(analyzer_instance):
    """
    Corre todos los tests usando un analizador personalizado.
    Útil para desarrolladores que quieran evaluar su implementación.
    """
    run_all_samples(analyzer_instance)
