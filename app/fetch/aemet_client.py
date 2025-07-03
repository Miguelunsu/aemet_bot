import os
import requests
import time

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
    print("Esperando 3 segundos... (1)")
    time.sleep(3)
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    print("Esperando 3 segundos... (2)")
    time.sleep(3)
    data = response.json()
    print(f"Descripción feedback: {data.get('descripcion')}")
    print(f"Path de datos tiemo real: {data['datos']}")
    print("Continuando.")
    return data['datos']

def download_data_from_url(data_url):
    response = requests.get(data_url)
    response.raise_for_status()
    return response.json()