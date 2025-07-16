# testing/test_runner.py

"""
Este módulo contiene funciones listas para ejecutar pruebas sobre analizadores ECG.
No requiere argumentos CLI. Solo importa y ejecuta lo que necesites.
"""

from app.services.PeakIntervalAnalyzer.PeakIntervalAnalyzer import PeakIntervalAnalyzer
from testing.ecg_benchmark import run_single_sample, run_all_samples, run_with_custom_analyzer


def test_single_sample(code="08405", plot=True):
    """
    Analiza un solo sample usando el analizador por defecto.
    """
    analyzer = PeakIntervalAnalyzer(sample_rate=300)
    run_single_sample(code, analyzer, plot=plot)


def test_all_samples(plot=False):
    """
    Analiza todos los samples disponibles.
    """
    analyzer = PeakIntervalAnalyzer(sample_rate=300)
    run_all_samples(analyzer, plot=plot)


def test_custom_analyzer(analyzer_instance):
    """
    Ejecuta pruebas completas con un analizador personalizado.
    """
    run_with_custom_analyzer(analyzer_instance)


# 👇 Puedes probar aquí directo si corres este archivo
if __name__ == "__main__":
    test_single_sample("04908", plot=True)
    # test_all_samples()
    # test_custom_analyzer(MyAnalyzer())
