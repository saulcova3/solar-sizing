import sys
import os
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.pvgis import get_pvgis_data, parse_hourly_radiation, clean_and_enrich, compute_daily_stats
from src.model import build_solar_model, recomendar_paneles

st.set_page_config(
    page_title="Solar Sizing",
    page_icon="☀️",
    layout="centered"
)
st.title("☀️ Dimensionamiento Bayesiano de Paneles Solares")
st.markdown("Estima cuántos paneles solares necesitas con incertidumbre cuantificada.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    lat = st.number_input("Latitud", value=8.6, format="%.4f")
    lon = st.number_input("Longitud", value=-63.9, format="%.4f")

with col2:
    consumo = st.number_input("Consumo mensual (kWh)", value=300, min_value=50, max_value=2000, step=50)
    p_panel = st.number_input("Potencia del panel (kW)", value=0.45, min_value=0.1, max_value=1.0, format="%.2f")

st.divider()

correr = st.button("Calcular", type="primary")

if correr:
    with st.spinner("Obteniendo datos de irradiación solar..."):
        raw = get_pvgis_data(lat=lat, lon=lon)
        df = parse_hourly_radiation(raw)
        df = clean_and_enrich(df)
        stats = compute_daily_stats(df)

    st.success(f"Irradiación media: {stats['H_mean']:.3f} kWh/m²/día")

    with st.spinner("Corriendo modelo bayesiano..."):
        modelo, trace = build_solar_model(
            stats["H_mean"],
            stats["H_std"],
            consumo_mensual_kwh=consumo,
            P_panel_kw=p_panel
        )
        recomendacion = recomendar_paneles(trace)

    st.divider()
    st.subheader("Resultados")

    col1, col2, col3 = st.columns(3)
    col1.metric("Paneles esperados", f"{recomendacion['N_medio']}")
    col2.metric("Intervalo 95%", f"[{recomendacion['N_min']}, {recomendacion['N_max']}]")
    col3.metric("Recomendado", f"{recomendacion['N_recomendado']} paneles")

    st.divider()
    st.subheader("Distribución posterior")

    N_muestras = trace.posterior["N"].values.flatten()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.hist(N_muestras, bins=50, color="#2196F3", alpha=0.7, edgecolor="white")
    ax.axvline(recomendacion["N_medio"], color="#FF5722", linewidth=2,
               label=f"Media: {recomendacion['N_medio']}")
    ax.axvline(recomendacion["N_min"], color="#4CAF50", linewidth=1.5,
               linestyle="--", label=f"IC 95%: [{recomendacion['N_min']}, {recomendacion['N_max']}]")
    ax.axvline(recomendacion["N_max"], color="#4CAF50", linewidth=1.5, linestyle="--")
    ax.axvline(recomendacion["N_recomendado"], color="#9C27B0", linewidth=2,
               linestyle="-.", label=f"Recomendado: {recomendacion['N_recomendado']}")
    ax.set_xlabel("Número de paneles")
    ax.set_ylabel("Frecuencia")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)