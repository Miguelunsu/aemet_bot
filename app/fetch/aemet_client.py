import os
import requests
import time
import logging

def get_api_key():
    api_key = os.getenv("AEMET_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la API key en las variables de entorno")
    return api_key

def get_data_url_from_aemet(endpoint, max_retries=30, delay=8):
    logging.info("Iniciando get_data_url_from_aemet")
    api_key = get_api_key()
    headers = {
        "accept": "application/json",
        "api_key": api_key
    }
    attempts = 0
    while attempts < max_retries:
        try:
            logging.info(f"get_data_url_from_aemet: intento {attempts+1}/{max_retries} consultando endpoint")
            response = requests.get(endpoint, headers=headers)
            data = response.json()
            
            estado = data.get('estado')
            descripcion = data.get('descripcion')
            logging.info(f"Estado: {estado}, Descripción: {descripcion}")
            if estado == 200:
                # exito
                logging.info(f"Conexión exitosa de get_data_url_from_aemet. Path de datos tiempo real: {data['datos']}")
                return data['datos']
            elif estado == 401:
                # sin datos
                logging.warning(f"No autorizado ({estado}). Reintento")
                pass
            elif estado == 404:
                # sin datos
                logging.warning(f"Sin datos de get_data_url_from_aemet ({estado}). Se devuelve un string Nan")
                return "Nan"
            elif estado == 429:
                # nos hemos pasado del tiempo. añadimos tiempo
                logging.warning(f"Pasado de tiempo ({estado}). Espera de un minuto. Se añade un intento.")
                attempts = attempts-1
                time.sleep(60)
                continue
            else:
                raise ValueError(f"Estado inesperado: {estado}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error de red: {e}. Reintentando en {delay} segundos.")
        except ValueError as e:
            logging.error(f"Error de lógica: {e}")
            break

        time.sleep(delay)
        attempts += 1
        
    print(f"No se pudo obtener la URL de datos tras {max_retries} intentos. Devolviendo string NaN")
    return None
    
def download_data_from_url(data_url, max_retries=10, delay=8):
    logging.info(f"Iniciando download_data_from_url. Data url: {data_url}")
    if not data_url or str(data_url).lower() == "nan":
        logging.warning("Input: string NaN. Devolviendo None en download_data_from_url.")
        return None

    for intento in range(max_retries):
        try:
            time.sleep(1) # pequeño cooldown para la web de aemet, que lo necesita

            response = requests.get(data_url, timeout=30)
            # Si el servidor responde, pero con error 500, raise_for_status lanza excepción
            response.raise_for_status()

            # Si todo va bien:
            logging.info(f"Datos descargados correctamente en intento {intento}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            code = getattr(e.response, "status_code", None)
            logging.warning(f"Intento {intento}: error HTTP {code} -> {e}")

            # Si es un error 500-599 (servidor), reintentamos
            if code and 500 <= code < 600:
                time.sleep(delay * intento)  # backoff exponencial
                continue
            else:
                # Si es 400 o similar, no sirve reintentar
                break

        except requests.exceptions.Timeout:
            logging.warning(f"Intento {intento}: tiempo de espera agotado. Reintentando...")
            time.sleep(delay * intento)
            continue

        except requests.exceptions.ConnectionError:
            logging.warning(f"Intento {intento}: error de conexión. Reintentando...")
            time.sleep(delay * intento)
            continue

        except Exception as e:
            logging.error(f"Intento {intento}: error inesperado -> {e}")
            break
        
    time.sleep(delay)
    logging.error(f"No se pudo obtener la data tras {max_retries} intentos. Devolviendo None.")
    return None