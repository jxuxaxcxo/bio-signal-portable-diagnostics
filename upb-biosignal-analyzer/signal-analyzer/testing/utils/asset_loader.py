import json
import os

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
