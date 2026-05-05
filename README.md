# ☀️ Solar Sizing — Dimensionamiento Bayesiano de Paneles Solares

Herramienta para estimar el número óptimo de paneles solares necesarios
dado el consumo eléctrico y la ubicación geográfica del usuario,
con incertidumbre cuantificada mediante un modelo bayesiano.

## ¿Por qué bayesiano?

La mayoría de calculadoras solares dan un número puntual. Este proyecto
entrega una distribución de probabilidad — "necesitas entre 4 y 8 paneles,
con mayor probabilidad en 6 o 7" — porque la irradiación solar varía año
a año y el consumo real es incierto.

## Stack

- **PyMC** — modelado bayesiano con MCMC (NUTS sampler)
- **PVGIS API** — datos históricos de irradiación solar (Comisión Europea)
- **Streamlit** — dashboard interactivo
- **matplotlib** — visualización del posterior

## Instalación

```bash
git clone https://github.com/saulcova3/solar-sizing
cd solar-sizing
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app/streamlit_app.py
```

## Estructura

```
solar-sizing/
├── app/
│   └── streamlit_app.py   # Dashboard
├── notebooks/
│   └── exploracion.py     # Exploración y visualización
├── src/
│   ├── pvgis.py           # Pipeline de extracción PVGIS
│   └── model.py           # Modelo bayesiano
└── requirements.txt
```
## Autor

Saul Cova — [linkedin.com/in/saul-cova-008830145](https://linkedin.com/in/saul-cova-008830145)

