import os
import requests
import time

def get_api_key():
    api_key = os.getenv("AEMET_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API key en las variables de entorno")
    return api_key

def get_data_url_from_aemet(endpoint, max_retries=20, delay=5):
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "api_key": api_key
    }
    attempts = 0
    while attempts < max_retries:
        try:
            print(f"Intento {attempts+1}/{max_retries} consultando endpoint")
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f"Descripción feedback: {data.get('descripcion')}")
            print(f"Path de datos tiempo real: {data['datos']}")
            print("Conexión exitosa.")
            return data['datos']
        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse a AEMET: {e}")
            print(f"Reintentando en {delay} segundos.")
            time.sleep(delay)
            attempts += 1
    raise RuntimeError(f"No se pudo obtener la URL de datos tras {max_retries} intentos.")

def download_data_from_url(data_url):
    response = requests.get(data_url)
    response.raise_for_status()
    return response.json()