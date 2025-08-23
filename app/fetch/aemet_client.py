import os
import requests
import time

import logging


def get_api_key():
    api_key = os.getenv("AEMET_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API key en las variables de entorno")
    return api_key

def get_data_url_from_aemet(endpoint, max_retries=20, delay=5):
    logging.info("Iniciando get_data_url_from_aemet")
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
            data = response.json()
            
            estado = data.get('estado')
            descripcion = data.get('descripcion')
            print(f"Estado: {estado}, Descripción: {descripcion}")
            if estado == 200:
                # exito
                logging.info(f"Conexión exitosa de get_data_url_from_aemet. Path de datos tiempo real: {data['datos']}")
                return data['datos']
            elif estado == 401:
                # sin datos
                print(f"No autorizado ({estado}). Reintento")
                pass
            elif estado == 404:
                # sin datos
                logging.info(f"Sin datos de get_data_url_from_aemet ({estado}). Se devuelve un string Nan")
                return "Nan"
            elif estado == 429:
                # Nos hemos pasado del tiempo. añadimos tiempo
                print(f"Pasado de tiempo ({estado}). Espera de un minuto. Se añade un intento.")
                attempts = attempts-1
                time.sleep(60)
                continue
            else:
                raise ValueError(f"Estado inesperado: {estado}")
        except requests.exceptions.RequestException as e:
            print(f"Error de red: {e}. Reintentando en {delay} segundos.")
        except ValueError as e:
            print(f"Error de lógica: {e}")
            break

        time.sleep(delay)
        attempts += 1
        
    print(f"No se pudo obtener la URL de datos tras {max_retries} intentos. Devolviendo string NaN")
    return "Nan"
    
def download_data_from_url(data_url, retries=3, delay=5):
    logging.info(f"Iniciando download_data_from_url. Data url: {data_url}")
    if data_url == "Nan":
        logging.info("Input: string Nan. Devolviendo un string Nan en download_data_from_url.")
        return "Nan"
    for intento in range(retries):
        try:
            response = requests.get(data_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.info(f"Intento {intento+1} fallido por error de red: {e}")
        except Exception as e:
            logging.info(f"Intento {intento+1} fallido por error inesperado: {e}")
        time.sleep(delay)
    logging.info(f"No se pudo obtener la data tras {retries} intentos. Devolviendo string NaN")
    return "Nan"