from src.universe_selector import select_universe
from src.data_loader import get_data
from src.data_cleaner import clean_data
from src.feature_engineering import compute_features
from src.scoring import score_magic_formula, score_multifactorial

# Paso 1: Selección de universo
tickers, market_caps = select_universe(min_market_cap=1_000_000_000_000, force_update=False)

# Paso 2: Descarga de datos
datasets = get_data(tickers, force_update=True)

# Paso 3: Limpieza de data (profile)
df_clean = clean_data(datasets["profile"], market_caps)

# Paso 4: Cálculo de métricas financieras
df_features  = compute_features(df_clean, datasets["income"], datasets["balance"], datasets["ev"])

# Paso 5A: Ranking clásico de Magic Formula
df_magic = score_magic_formula(df_features)
print(f"\tTop Magic Formula")
# print(df_magic.head(10))

# Paso 5B: Ranking multifactorial
weights = {
    "ROIC": 1.0,
    "EarningsYield": 1.0,
    "EBITMargin": 0.0,
    "ROE": 0.0,
    "Beta": 0.0  # Menor beta = mejor (control de riesgo)
}


df_multi = score_multifactorial(df_features, weights)
print(f"\tTop Scoring Multifactorial")
# print(df_multi.head(10))