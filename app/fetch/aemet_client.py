import os
import requests

def get_api_key():
    api_key = os.getenv("AEMET_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API key en las variables de entorno")
    return api_key

def get_data_url_from_aemet(endpoint):
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "api_key": api_key
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"Path de datos tiemo real: {data['datos']}")
    return data['datos']

def download_data_from_url(data_url):
    response = requests.get(data_url)
    response.raise_for_status()
    return response.json()