from abc import ABC, abstractmethod
import numpy as np

class ECGAnalyzerInterface(ABC):


    @abstractmethod
    def analyze(self, ecg_data: np.ndarray) -> dict:
        """
        Ejecuta el análisis de una señal ECG.

        Parámetros:
        - ecg_data (np.ndarray): Señal ECG como arreglo de floats.

        Retorna:
        - dict: Un diccionario con resultados del análisis. Puede incluir métricas, flags de detección, etc.
        """
        pass
