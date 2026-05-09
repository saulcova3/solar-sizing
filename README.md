# ☀️ Solar Sizing — Dimensionamiento cuasi-bayesiano de Paneles Solares

Herramienta para estimar el número óptimo de paneles solares necesarios
dado el consumo eléctrico y la ubicación geográfica del usuario,
con incertidumbre cuantificada mediante propagación probabilística.

## ¿Por qué propagación de incertidumbre?

La mayoría de calculadoras solares dan un número puntual. Este proyecto
entrega una distribución de probabilidad — "necesitas entre 4 y 8 paneles,
con mayor probabilidad en 6 o 7" — porque la irradiación solar varía año
a año y el consumo real es incierto.

### ¿Qué hace realmente el modelo?

1. Toma la media y varianza histórica de irradiación solar de PVGIS
2. Construye una distribución de posibles valores de irradiación
3. Incorpora incertidumbre sobre la eficiencia del sistema (pérdidas)
4. Propaga ambas incertidumbres a través de la fórmula física
   `N = consumo / (potencia × irradiación × eficiencia)`
5. Entrega la distribución resultante del número de paneles

**Nota metodológica**: Este es un modelo de **propagación de incertidumbre**
(uncertainty propagation) usando priors probabilísticos informados por datos
históricos. Actualmente no incluye una etapa de verosimilitud (likelihood)
que permita actualizar las creencias con datos observados, por lo que no
constituye inferencia bayesiana completa.

## Stack

- **PyMC** — muestreo probabilístico con MCMC (NUTS sampler)
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
python -m streamlit run app/streamlit_app.py
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

