import pandas as pd

def clean_data(raw_data, market_caps_dict):
    """
    Convierte el diccionario crudo de FMP en un DataFrame ordenado,
    incorporando el Market Cap desde Yahoo Finance.
    
    Parameters:
    - raw_data: diccionario FMP (profile).
    - market_caps_dict: diccionario {ticker: market_cap} proveniente de Yahoo.
    
    Returns:
    - DataFrame limpio y ordenado.
    """
    rows = []

    for ticker, data in raw_data.items():
        rows.append({
            "Ticker": ticker,
            "CompanyName": data.get("companyName", None),
            "Sector": data.get("sector", None),
            "Industry": data.get("industry", None),
            "Price": data.get("price", None),
            "MarketCap": market_caps_dict.get(ticker),  # usamos el dato real
            "Beta": data.get("beta", None)
        })
    
    df = pd.DataFrame(rows)
    return df


def _safe_float(value):
    """
    Convierte un valor a float, devuelve None si no se puede convertir.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
