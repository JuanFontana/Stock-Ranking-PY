import os
import json
import requests
import yaml

# Leer configuración
with open("config/settings.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["fmp_api_key"]

DATA_PATHS = {
    "profile": "data/raw/data_profile.json",
    "income": "data/raw/data_income.json",
    "balance": "data/raw/data_balance.json",
    "ev": "data/raw/data_ev.json"
}


def get_data(tickers, force_update=False):
    """
    Descarga o carga los datasets necesarios desde FMP (versión stable) para los tickers proporcionados.
    Devuelve un diccionario con los 4 datasets: profile, income, balance y ev.
    """
    datasets = {}

    datasets["profile"] = load_or_download(tickers, "profile", force_update)
    datasets["income"] = load_or_download(tickers, "income", force_update)
    datasets["balance"] = load_or_download(tickers, "balance", force_update)
    datasets["ev"] = load_or_download(tickers, "ev", force_update)

    return datasets


def load_or_download(tickers, dataset_name, force_update):
    file_path = DATA_PATHS[dataset_name]

    if os.path.exists(file_path) and not force_update:
        print(f"Cargando {dataset_name} desde archivo local...")
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        print(f"Descargando {dataset_name} desde FMP...")
        data = download_dataset_from_fmp(tickers, dataset_name)
        os.makedirs("data/raw", exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    return data


def download_dataset_from_fmp(tickers, dataset_name):
    """
    Descarga el dataset específico desde FMP (versión stable) para todos los tickers.
    """
    data = {}

    for ticker in tickers:
        if dataset_name == "profile":
            url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={API_KEY}"
        elif dataset_name == "income":
            url = f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={API_KEY}"
        elif dataset_name == "balance":
            url = f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={API_KEY}"
        elif dataset_name == "ev":
            url = f"https://financialmodelingprep.com/stable/enterprise-values?symbol={ticker}&apikey={API_KEY}"
        else:
            raise ValueError("Nombre de dataset no reconocido.")

        try:
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                if json_data:
                    data[ticker] = json_data[0]  # Tomamos solo el dato más reciente
                else:
                    print(f"No se encontró información para {ticker} en {dataset_name}")
            else:
                print(f"Error al descargar {ticker} ({dataset_name}): {response.status_code}")
        except Exception as e:
            print(f"Error con {ticker} en {dataset_name}: {e}")
    
    return data
