import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.pvgis import get_pvgis_data, parse_hourly_radiation, clean_and_enrich, compute_daily_stats
from src.model import build_solar_model, recomendar_paneles


def plot_posterior_paneles(trace, recomendacion):
    """
    Grafica la distribución posterior del número de paneles.
    """
    N_muestras = trace.posterior["N"].values.flatten()

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(N_muestras, bins=50, color="#2196F3", alpha=0.7, edgecolor="white")

    # Línea del valor esperado
    ax.axvline(recomendacion["N_medio"], color="#FF5722", linewidth=2,
               label=f"Media: {recomendacion['N_medio']}")

    # Intervalo de credibilidad 95%
    ax.axvline(recomendacion["N_min"], color="#4CAF50", linewidth=1.5,
               linestyle="--", label=f"IC 95%: [{recomendacion['N_min']}, {recomendacion['N_max']}]")
    ax.axvline(recomendacion["N_max"], color="#4CAF50", linewidth=1.5,
               linestyle="--")

    # Línea de recomendación
    ax.axvline(recomendacion["N_recomendado"], color="#9C27B0", linewidth=2,
               linestyle="-.", label=f"Recomendado: {recomendacion['N_recomendado']}")

    ax.set_xlabel("Número de paneles", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title("Distribución posterior — Paneles solares necesarios", fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig("notebooks/posterior_paneles.png", dpi=150)
    plt.show()
    print("Gráfica guardada en notebooks/posterior_paneles.png")


if __name__ == "__main__":
    print("Obteniendo datos de PVGIS...")
    raw = get_pvgis_data(lat=8.6, lon=-63.9)
    df = parse_hourly_radiation(raw)
    df = clean_and_enrich(df)
    stats = compute_daily_stats(df)

    print(f"H_mean: {stats['H_mean']:.3f} kWh/m²/día")
    print(f"H_std:  {stats['H_std']:.3f} kWh/m²/día")

    print("\nCorriendo modelo bayesiano...")
    modelo, trace = build_solar_model(
        stats["H_mean"],
        stats["H_std"],
        consumo_mensual_kwh=300
    )

    recomendacion = recomendar_paneles(trace)
    print(f"\nN esperado:    {recomendacion['N_medio']} paneles")
    print(f"Intervalo 95%: [{recomendacion['N_min']}, {recomendacion['N_max']}]")
    print(f"N recomendado: {recomendacion['N_recomendado']} paneles")

    plot_posterior_paneles(trace, recomendacion)