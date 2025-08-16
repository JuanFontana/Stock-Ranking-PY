# src/scoring.py

import pandas as pd

def score_magic_formula(df):
    """
    Scoring clásico de Greenblatt basado en ROIC y Earnings Yield.
    """
    df = df.copy()
    df = df.dropna(subset=["ROIC", "EarningsYield"])

    df["Rank_ROIC"] = df["ROIC"].rank(ascending=False, method="min")
    df["Rank_EarningsYield"] = df["EarningsYield"].rank(ascending=False, method="min")

    df["MagicFormulaScore"] = df["Rank_ROIC"] + df["Rank_EarningsYield"]
    df["Rank_Final"] = df["MagicFormulaScore"].rank(ascending=True, method="min")

    return df.sort_values("Rank_Final").reset_index(drop=True)


def score_multifactorial(df, weights):
    """
    Modelo multifactorial con pesos configurables.
    Aplica rankeo y combina por score ponderado.
    """
    df = df.copy()
    # Filtramos filas que no tengan ninguna variable necesaria
    relevant_cols = list(weights.keys())
    df = df.dropna(subset=relevant_cols, how="any")

    # Rankeo y ponderación
    for factor in relevant_cols:
        ascending = weights[factor] < 0  # Si el peso es negativo, rankeo ascendente (riesgo bajo = mejor)
        df[f"Rank_{factor}"] = df[factor].rank(ascending=ascending, method="min")

    # Scoring total
    df["MultiFactorScore"] = sum(
        weights[f] * df[f"Rank_{f}"] for f in relevant_cols
    )

    df["Rank_Final"] = df["MultiFactorScore"].rank(ascending=True, method="min")

    return df.sort_values("Rank_Final").reset_index(drop=True)
