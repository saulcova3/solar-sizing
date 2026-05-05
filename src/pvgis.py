import requests
import pandas as pd

PVGIS_URL = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"


def get_pvgis_data(lat, lon, startyear=2015, endyear=2023):
    """
    Consulta la API de PVGIS y devuelve el JSON crudo.

    Parámetros:
        lat: latitud de la ubicación
        lon: longitud de la ubicación
        startyear: año de inicio del histórico
        endyear: año de fin del histórico
    """
    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": 1,
        "loss": 14,
        "outputformat": "json",
        "startyear": startyear,
        "endyear": endyear,
        "components": 1,
    }

    response = requests.get(PVGIS_URL, params=params)
    response.raise_for_status()

    return response.json()


def parse_hourly_radiation(raw_json):
    """
    Extrae los datos horarios del JSON crudo y los estructura en un DataFrame.

    Retorna un DataFrame con columnas:
        - time: timestamp
        - P: potencia generada (W)
        - Gb: irradiación directa (W/m²)
        - Gd: irradiación difusa (W/m²)
        - T2m: temperatura a 2m (°C)
    """
    hourly_data = raw_json["outputs"]["hourly"]
    df = pd.DataFrame(hourly_data)
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M")
    df = df.set_index("time")

    return df


def compute_daily_stats(df):
    """
    Agrega los datos horarios a nivel diario y calcula
    media y desviación estándar de la irradiación.

    Retorna un diccionario con:
        - daily_df: DataFrame con irradiación total por día
        - H_mean: media diaria histórica (kWh/m²/día)
        - H_std: desviación estándar diaria histórica
    """
    daily_df = df[["Gb(i)", "Gd(i)"]].resample("D").sum() / 1000
    daily_df["H"] = daily_df["Gb(i)"] + daily_df["Gd(i)"]

    H_mean = daily_df["H"].mean()
    H_std = daily_df["H"].std()

    return {
        "daily_df": daily_df,
        "H_mean": H_mean,
        "H_std": H_std,
    }

def clean_and_enrich(df):
    """
    Limpia y enriquece el DataFrame horario.

    - Elimina filas con valores negativos (errores de sensor)
    - Agrega columna de mes para análisis estacional
    - Agrega columna de hora para análisis diurno
    """
    # Valores negativos son errores — los reemplazamos con 0
    df[["Gb(i)", "Gd(i)"]] = df[["Gb(i)", "Gd(i)"]].clip(lower=0)

    # Columnas de contexto temporal
    df["month"] = df.index.month
    df["hour"] = df.index.hour

    return df

if __name__ == "__main__":
    raw = get_pvgis_data(lat=8.6, lon=-63.9)
    df = parse_hourly_radiation(raw)
    df = clean_and_enrich(df)
    stats = compute_daily_stats(df)

    print(f"H_mean: {stats['H_mean']:.3f} kWh/m²/día")
    print(f"H_std:  {stats['H_std']:.3f} kWh/m²/día")
    print(stats["daily_df"].head())