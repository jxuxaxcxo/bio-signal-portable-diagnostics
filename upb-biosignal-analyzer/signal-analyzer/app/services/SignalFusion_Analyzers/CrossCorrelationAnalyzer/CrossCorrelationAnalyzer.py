# app/services/SignalFusion_Analyzers/CrossCorrelationAnalyzer/CrossCorrelationAnalyzer.py

import numpy as np
from scipy.signal import correlate
from app.models.signal_fusion_models import SignalFusionInput, SignalFusionResult


class CrossCorrelationAnalyzer:

    def __init__(self, sample_rate: int = 1000):
        self.sample_rate = sample_rate  # Solo se usa si queremos convertir delays a segundos

    def analyze(self, fusion_input: SignalFusionInput) -> SignalFusionResult:
        ecg = fusion_input.ecg_features
        pcg = fusion_input.pcg_features

        # === Validaciones básicas ===
        if not ecg.peak_locations or not pcg.peak_locations:
            return SignalFusionResult(
                correlation_score=0.0,
                alignment_delay_sec=0.0,
                aligned_s1_to_r_count=0,
                aligned_s2_to_t_count=0,
                alignment_score=0.0,
                diagnostic_hint="Datos insuficientes para análisis",
                notes="Faltan picos en ECG o PCG"
            )

        # === Señales binarias de eventos ===
        ecg_signal_bin = np.zeros(int(ecg.duration_sec * self.sample_rate))
        pcg_signal_bin = np.zeros(int(pcg.duration_sec * self.sample_rate))

        for loc in ecg.peak_locations:
            if loc < len(ecg_signal_bin):
                ecg_signal_bin[loc] = 1

        for loc in pcg.peak_locations:
            if loc < len(pcg_signal_bin):
                pcg_signal_bin[loc] = 1

        # === Igualar longitudes ===
        min_len = min(len(ecg_signal_bin), len(pcg_signal_bin))
        ecg_signal_bin = ecg_signal_bin[:min_len]
        pcg_signal_bin = pcg_signal_bin[:min_len]

        # === Correlación cruzada ===
        correlation = correlate(pcg_signal_bin, ecg_signal_bin, mode='same', method='fft')
        lag_index = np.argmax(correlation)
        lag_samples = lag_index - len(ecg_signal_bin) // 2
        lag_seconds = lag_samples / self.sample_rate
        correlation_score = np.max(correlation) / (np.sum(ecg_signal_bin) or 1)

        # === Chequeo de alineamiento R→S1 y T→S2 ===
        aligned_s1 = 0
        aligned_s2 = 0
        tolerance = 0.15  # en segundos

        for r in ecg.peak_locations:
            r_time = r / self.sample_rate
            aligned_s1 += any(
                abs((s1 / self.sample_rate) - r_time) <= tolerance for s1 in pcg.s1_locations
            )

        for t in ecg.peak_locations:  # 👈 por ahora usamos R también como proxy de T
            t_time = t / self.sample_rate
            aligned_s2 += any(
                abs((s2 / self.sample_rate) - t_time) <= tolerance for s2 in pcg.s2_locations
            )

        total_beats = max(len(ecg.peak_locations), 1)
        alignment_score = (aligned_s1 + aligned_s2) / (2 * total_beats)

        # === Diagnóstico tentativo ===
        if alignment_score > 0.75:
            hint = "normal"
        elif alignment_score > 0.4:
            hint = "posible desincronización leve"
        else:
            hint = "desincronización severa"

        return SignalFusionResult(
            correlation_score=correlation_score,
            alignment_delay_sec=lag_seconds,
            aligned_s1_to_r_count=aligned_s1,
            aligned_s2_to_t_count=aligned_s2,
            alignment_score=alignment_score,
            diagnostic_hint=hint,
            notes=f"Desfase medio: {lag_seconds:.3f}s | Alineación: {alignment_score:.2%}"
        )
