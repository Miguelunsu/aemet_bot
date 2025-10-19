from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from fetch.extreme_values import get_station_max_last12h, get_station_sum_last12h
import logging

def get_12h_values(meteo_var):
    # data: diccionario que tiene todas las medidas en tiempo real (una por hora)
    # meteo_var: variable meteo de la que queremos los datos extremos por estacion
    
    # Devuelve: variable est_extreme_12h: Nested diccionary de estaciones con los datos de variable max.
    # Key: idema. Dentro: diccionario con fint (hora), tamax, ubi, lat y lon

    # encapsulado desde aqui: obtener max_temp_12h_estaciones

    # Endpoint de las medidas en tiempo real
    endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'

    # data_url: str con el enlace a los datos de 12 horas (e.g., https://opendata.aemet.es/opendata/sh/cfca0eb5)
    data_url = get_data_url_from_aemet(endpoint)
    # data: lista de diccionarios de estaciones meteo. Cada diccionario tiene toda la info de las 12 últimas horas
    data = download_data_from_url(data_url, retries=10)
    logging.info(f"Datos descargados. Lineas: {len(data)}")

    # Si el data es "nan" es que no se ha podido conectar nada
    if isinstance(data, str) and data.lower() == "nan":
        raise ValueError("La variable 'data' es un string 'Nan'. No se ha podido conectar.")
    
    # max_temp_12h_estaciones: nested diccionary de estaciones con los datos de la temperatura maxima. El dicc. contiene fint (hora), tamax, ubi, lat y lon
    if meteo_var == "tamax": # entonces queremos el maximo
        extreme_value_12h_estaciones = get_station_max_last12h(data, meteo_var=meteo_var)

        # PARA TESTING/TESTEAR: incluir artificialmente records
        extreme_value_12h_estaciones["0009X"]["value"] = 1000
    elif meteo_var == "prec": # entonces queremos la suma
        extreme_value_12h_estaciones = get_station_sum_last12h(data, meteo_var=meteo_var)
    logging.info(f"Valores extremos de T obtenidos. Número de estaciones encontradas: {len(extreme_value_12h_estaciones.keys())}")
    return extreme_value_12h_estaciones