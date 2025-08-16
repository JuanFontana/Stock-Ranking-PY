import pandas as pd
import yfinance as yf
import os
import json

MARKET_CAP_PATH = "data/raw/market_cap.json"

def get_sp500_tickers():
    """
    Descarga los tickers del S&P 500 desde Wikipedia.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    tickers = df["Symbol"].tolist()
    tickers = [ticker.replace('.', '-') for ticker in tickers]  # Ajuste para Yahoo Finance
    return tickers


def get_market_caps(tickers, force_update=False):
    """
    Obtiene el Market Cap de cada ticker desde Yahoo Finance.
    """
    if os.path.exists(MARKET_CAP_PATH) and not force_update:
        print("Cargando Market Cap desde archivo local...")
        with open(MARKET_CAP_PATH, "r") as f:
            return json.load(f)

    print("Descargando Market Cap desde Yahoo Finance...")
    market_caps = {}
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            market_cap = info.get("marketCap")
            if market_cap:
                market_caps[ticker] = market_cap
        except Exception as e:
            print(f"Error con {ticker}: {e}")

    os.makedirs("data/raw", exist_ok=True)
    with open(MARKET_CAP_PATH, "w") as f:
        json.dump(market_caps, f, indent=4)

    return market_caps


def filter_by_market_cap(market_caps, min_market_cap=10_000_000_000):
    """
    Filtra los tickers por Market Cap mínimo.
    """
    filtered = [ticker for ticker, cap in market_caps.items() if cap and cap >= min_market_cap]
    return filtered


def select_universe(min_market_cap=10_000_000_000, force_update=False):
    """
    Devuelve una lista de tickers filtrados por Market Cap y
    un diccionario con los Market Cap de cada uno.
    """
    print("Descargando tickers del S&P 500...")
    tickers = get_sp500_tickers()
    print(f"Total de tickers encontrados: {len(tickers)}")

    market_caps = get_market_caps(tickers, force_update=force_update)
    print(f"Market Cap disponible para {len(market_caps)} tickers.")

    filtered = [t for t in tickers if market_caps.get(t, 0) >= min_market_cap]
    print(f"Tickers seleccionados luego del filtro de Market Cap >= {min_market_cap}: {len(filtered)}")

    return filtered, market_caps
