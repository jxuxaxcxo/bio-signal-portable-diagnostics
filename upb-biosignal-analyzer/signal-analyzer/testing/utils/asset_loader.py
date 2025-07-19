import json
import os
import wfdb
import numpy as np

def load_assets_constants(json_file_path: str) -> dict:
    """
    Carga el archivo assetsConstants.json, que contiene los picos esperados por sample.

    Parámetros:
    - json_file_path (str): Ruta al archivo JSON

    Retorna:
    - dict: Diccionario con estructura {'Data': [{'Sample': sample_id, 'Peaks': value}, ...]}
    """
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"No se encontró el archivo de constantes: {json_file_path}")

    with open(json_file_path, 'r') as file:
        return json.load(file)


def load_assets_codes(json_file_path: str) -> list:
    """
    Carga la lista de códigos de samples desde el archivo assetsCodes.json.

    Parámetros:
    - json_file_path (str): Ruta al archivo JSON

    Retorna:
    - list: Lista de códigos de samples (strings)
    """
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"No se encontró el archivo de códigos de assets: {json_file_path}")

    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data.get("codes", [])
    

def load_sample_ecg_data(sample_code: str, format_hint: str = "wfdb", max_duration_sec: int = None) -> tuple:
    """
    Carga una señal ECG desde assets en distintos formatos.

    Parámetros:
    - sample_code (str): El nombre base del sample (sin extensión)
    - format_hint (str): 'wfdb', 'csv', 'json', etc.
    - max_duration_sec (int, opcional): Si se especifica, recorta el trazo a esa duración en segundos.

    Retorna:
    - (ecg_data, sample_rate)
    """
    base_path = os.path.join("testing", "testing-assets", "mit-bih-arrhythmia-database", sample_code, sample_code)

    if format_hint == "wfdb":
        try:
            record = wfdb.rdrecord(base_path)
            ecg_signal = record.p_signal[:, 0]  # Suponiendo canal 0
            sample_rate = record.fs

            if max_duration_sec:
                max_samples = int(max_duration_sec * sample_rate)
                ecg_signal = ecg_signal[:max_samples]

            return ecg_signal.tolist(), sample_rate
        except Exception as e:
            raise FileNotFoundError(f"No se pudo leer el archivo WFDB en {base_path}: {e}")

    elif format_hint == "csv":
        csv_path = base_path + ".csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"No se encontró el archivo CSV: {csv_path}")
        data = np.loadtxt(csv_path, delimiter=",")
        if max_duration_sec:
            sample_rate = 300
            max_samples = int(max_duration_sec * sample_rate)
            data = data[:max_samples]
        return data.tolist(), 300

    elif format_hint == "json":
        json_path = base_path + ".json"
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"No se encontró el archivo JSON: {json_path}")
        with open(json_path, 'r') as f:
            obj = json.load(f)
        data = obj["data"]
        sample_rate = obj.get("sample_rate", 300)
        if max_duration_sec:
            max_samples = int(max_duration_sec * sample_rate)
            data = data[:max_samples]
        return data, sample_rate

    else:
        raise ValueError(f"Formato no soportado: {format_hint}")
