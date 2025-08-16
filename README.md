# 🧠 Magic Formula Quant Project

Este proyecto implementa la estrategia de inversión "Magic Formula" de Joel Greenblatt con un enfoque cuantitativo moderno, incluyendo:

- Selección de universo de acciones (S&P 500)
- Descarga eficiente de datos financieros desde Financial Modeling Prep (FMP)
- Limpieza y estandarización de datos
- Cálculo de métricas financieras clave
- Ranking clásico (Greenblatt puro)
- Ranking multifactorial con pesos personalizables
- Control de riesgo mediante Beta, Volatilidad, y otras métricas (opcional)

---

## 🎯 Objetivo

Detectar empresas atractivas para invertir combinando:
- Alta rentabilidad sobre el capital (ROIC)
- Valoraciones atractivas (Earnings Yield)
- Factores adicionales como FCF Yield, EV/Sales, ROE, Beta, etc.

---

## 📦 Estructura del proyecto

```
magic_formula_quant/
├── data/                       # Carpeta donde se almacenan los datos locales
│   ├── raw/                    # Archivos .json descargados desde FMP
│   │   └── data.json           # Data completa combinada
├── src/                        # Código fuente
│   ├── universe_selector.py    # Selección del universo base (S&P 500 filtrado)
│   ├── data_loader.py          # Descarga datos desde FMP y los guarda por módulo
│   ├── data_cleaner.py         # Limpieza del dataset inicial (profile)
│   ├── feature_engineering.py  # Cálculo de métricas como ROIC, EY, ROE, etc.
│   ├── scoring.py              # Implementa el ranking Magic Formula y multifactorial
│   ├── config.py               # Configuración de API key y variables generales
│   └── utils.py                # Funciones auxiliares
├── main.py                     # Pipeline principal del proyecto
├── requirements.txt            # Librerías necesarias
└── README.md                   # Documentación
```

---

## 🔧 Configuración

1. Crea el archivo `config.py` en `src/` con:
```python
API_KEY = "TU_API_KEY_FMP"
UNIVERSE = "SP_500"
```

2. Instala dependencias:
```bash
pip install -r requirements.txt
```

---

## 🚀 Cómo ejecutar

Desde el root del proyecto, ejecutá:

```bash
python main.py
```

El flujo es:

1. Selección del universo (`select_universe`)
2. Descarga los datos financieros (`get_data`)
3. Limpieza del dataset (`clean_data`)
4. Cálculo de métricas (`compute_features`)
5. Ranking (clásico y multifactorial)

---

## 📂 Descripción de cada módulo

### `src/universe_selector.py`
- Descarga la lista del S&P 500 desde Wikipedia.
- Obtiene el Market Cap de cada ticker desde Yahoo Finance.
- Guarda los resultados en `market_cap.json`.
- Parámetro:
  - `min_market_cap`: filtra empresas con mínimo tamaño.
  - `force_update`: si `True`, fuerza descarga aunque exista json local.

### `src/data_loader.py`
- Descarga datos de FMP:
  - Profile
  - Income Statement
  - Balance Sheet
  - Enterprise Value
- Usa caché local para evitar consumir requests.
- Parámetro `force_update`: si es `True`, descarga nuevamente.

### `src/data_cleaner.py`
- Toma los datos de `profile` y genera un DataFrame limpio.
- Filtra columnas necesarias: `Ticker`, `CompanyName`, `Sector`, `Beta`, etc.

### `src/feature_engineering.py`
- Calcula métricas clave:
  - ROIC
  - Earnings Yield
  - EBIT Margin
  - ROE
  - FCF Yield
  - EV/Sales
  - Beta
- Limpia duplicados como `Beta_x` y `Beta_y`.

### `src/scoring.py`
- `score_magic_formula(df)`: Ranking puro de Greenblatt usando ROIC + EY.
- `score_multifactorial(df, weights_dict)`: Modelo multivariable con pesos personalizables para cada métrica.

---

## 📊 Variables importantes

### Dentro de `main.py`:

- `tickers = select_universe(min_market_cap=...)` → Define el universo.
- `datasets = get_data(tickers, force_update=True)` → Descarga info de FMP.
- `df_clean` → DataFrame limpio (profile).
- `df_features` → DataFrame con todas las métricas financieras calculadas.
- `weights = {...}` → Diccionario de pesos para el ranking multifactorial.

---

## 📈 Ejemplo de pesos multifactoriales

```python
weights = {
    "ROIC": 0.3,
    "EarningsYield": 0.3,
    "EBITMargin": 0.2,
    "ROE": 0.1,
    "Beta": -0.1  # Menor beta = mejor
}
```

---

## 🔮 Posibles mejoras futuras

- Calcular `Volatility` con precios de Yahoo Finance
- Calcular `Altman Z-Score` desde balances
- Incorporar otros factores: crecimiento, calidad de management, etc.
- Visualizaciones interactivas (Streamlit, Dash)
- Backtesting con históricos

---

## 📞 Contacto

Cualquier duda o sugerencia, podés abrir un issue o contactarme.