import pymc as pm
import numpy as np

def build_solar_model(H_mean, H_std, consumo_mensual_kwh, P_panel_kw=0.45):
    """
    Modelo bayesiano para dimensionamiento de paneles solares.

    Parámetros:
        H_mean: irradiación media diaria histórica (kWh/m²/día)
        H_std: desviación estándar de la irradiación histórica
        consumo_mensual_kwh: consumo mensual del usuario en kWh
        P_panel_kw: potencia nominal de cada panel en kW (default 0.45)

    Retorna:
        modelo PyMC y trace con muestras del posterior
    """
    consumo_diario = consumo_mensual_kwh / 30

    with pm.Model() as solar_model:

        # Prior sobre irradiación — Normal centrada en el histórico
        H = pm.Normal("H", mu=H_mean, sigma=H_std)

        # Prior sobre eficiencia del sistema — Beta entre 0.75 y 0.85
        eta = pm.Beta("eta", alpha=20, beta=4)

        # Número de paneles necesarios — cantidad continua por ahora
        N = pm.Deterministic("N", consumo_diario / (P_panel_kw * H * eta))

        # Muestreamos el posterior
        trace = pm.sample(1000, tune=500, progressbar=True, return_inferencedata=True)

    return solar_model, trace

def recomendar_paneles(trace):
    """
    Interpreta el posterior y devuelve una recomendación concreta.

    Retorna un diccionario con:
        - N_medio: número esperado de paneles
        - N_min: límite inferior con 95% de credibilidad
        - N_max: límite superior con 95% de credibilidad
        - N_recomendado: entero conservador para la instalación
    """
    N_muestras = trace.posterior["N"].values.flatten()

    N_medio = float(np.mean(N_muestras))
    N_min = float(np.percentile(N_muestras, 2.5))
    N_max = float(np.percentile(N_muestras, 97.5))
    N_recomendado = int(np.ceil(np.percentile(N_muestras, 90)))

    return {
        "N_medio": round(N_medio, 2),
        "N_min": round(N_min, 2),
        "N_max": round(N_max, 2),
        "N_recomendado": N_recomendado,
    }

if __name__ == "__main__":
    # Valores de prueba — Ciudad Guayana, consumo típico hogar pequeño
    H_mean = 5.296
    H_std = 0.914
    consumo_mensual = 300  # kWh/mes

    modelo, trace = build_solar_model(H_mean, H_std, consumo_mensual)
    recomendacion = recomendar_paneles(trace)

    print(f"\nConsumo mensual: {consumo_mensual} kWh/mes")
    print(f"N esperado:      {recomendacion['N_medio']} paneles")
    print(f"Intervalo 95%:   [{recomendacion['N_min']}, {recomendacion['N_max']}]")
    print(f"N recomendado:   {recomendacion['N_recomendado']} paneles")