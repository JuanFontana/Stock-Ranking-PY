import pandas as pd

def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def compute_features(df_clean, income_data, balance_data, ev_data):
    """
    Calcula las métricas financieras necesarias para la Magic Formula clásica
    y el modelo de scoring multifactorial.
    """
    features = []

    for _, row in df_clean.iterrows():
        ticker = row["Ticker"]

        try:
            income = income_data.get(ticker, {})
            balance = balance_data.get(ticker, {})
            ev = ev_data.get(ticker, {})

            # Datos financieros
            ebit = _safe_float(income.get("ebit"))
            revenue = _safe_float(income.get("revenue"))
            net_income = _safe_float(income.get("netIncome"))
            fcf = _safe_float(income.get("freeCashFlow"))

            total_assets = _safe_float(balance.get("totalAssets"))
            total_equity = _safe_float(balance.get("totalStockholdersEquity"))
            current_liabilities = _safe_float(balance.get("totalCurrentLiabilities"))
            net_ppe = _safe_float(balance.get("propertyPlantEquipmentNet"))

            enterprise_value = _safe_float(ev.get("enterpriseValue"))
            ev_revenue = _safe_float(ev.get("revenue"))

            # ROIC
            capital_employed = (total_assets - current_liabilities - net_ppe) if total_assets and current_liabilities and net_ppe else None
            roic = ebit / capital_employed if ebit and capital_employed and capital_employed != 0 else None

            # Earnings Yield
            earnings_yield = ebit / enterprise_value if ebit and enterprise_value and enterprise_value != 0 else None

            # EBIT Margin
            ebit_margin = ebit / revenue if ebit and revenue and revenue != 0 else None

            # ROE
            roe = net_income / total_equity if net_income and total_equity and total_equity != 0 else None

            # FCF Yield
            fcf_yield = fcf / enterprise_value if fcf and enterprise_value and enterprise_value != 0 else None

            # EV / Sales
            ev_sales = enterprise_value / ev_revenue if enterprise_value and ev_revenue and ev_revenue != 0 else None

            # Beta (desde df_clean)
            beta = _safe_float(row.get("Beta"))

            # Volatilidad histórica (placeholder)
            volatility = None  # implementar luego

            # Altman Z-Score (placeholder)
            altman_z = None  # implementar luego

            features.append({
                "Ticker": ticker,
                "ROIC": roic,
                "EarningsYield": earnings_yield,
                "EBITMargin": ebit_margin,
                "ROE": roe,
                "FCFYield": fcf_yield,
                "EVSales": ev_sales,
                "Volatility": volatility,
                "AltmanZ": altman_z
            })

        except Exception as e:
            print(f"Error calculando métricas para {ticker}: {e}")

    df_features = pd.DataFrame(features)
    df_final = df_clean.merge(df_features, on="Ticker", how="left")

    
    # ✅ Limpiar columnas Beta duplicadas si existen
    if "Beta_x" in df_final.columns and "Beta_y" in df_final.columns:
        df_final = df_final.drop(columns=["Beta_y"])
        df_final = df_final.rename(columns={"Beta_x": "Beta"})
        
    return df_final
