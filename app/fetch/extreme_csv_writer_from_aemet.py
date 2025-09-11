import logging
import time
import os
import datetime

from fetch.csv_reader import estacion_reader
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from utils.parser import parser_temp_max_todos_meses
from utils.csv_writer import csv_writer_tmax_todos_meses

# Lectura temperaturas extremas de la aemet
def lectura_tmax_absolutas_aemet(BASE_DIR):
    # Leyendo datos de todas las estaciones
    ruta_csv_estaciones = os.path.join(BASE_DIR, "estaciones.csv")
    datos_estaciones = estacion_reader(ruta_csv_estaciones)

    # Nombre del csv de tmax_estaciones_ con la fecha
    nombre_tmax_csv = "tmax_estaciones_" + datetime.datetime.now().strftime('%Y%m%d') + ".csv"

    # counter de las estaciones
    i_counter = 0
    # Bucle temperaturas extremas
    for i_estacion in datos_estaciones:
        i_counter = i_counter + 1
        i_idema = i_estacion.get("idema")

        logging.info(f"Estudiando Tmax en station: {i_idema}. Station {i_counter}/{len(datos_estaciones)}")
        logging.info("Time sleep: 3")
        time.sleep(3)

        # Endpoint para valores extremos de temperatura
        endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{i_idema}'
        data_url = get_data_url_from_aemet(endpoint)

        logging.info(f"Estacion: {i_idema} -> data_url tempext: {data_url}")
        data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
        
        dicc_estacion_tmax = parser_temp_max_todos_meses(data)

        file_name = os.path.join(BASE_DIR, nombre_tmax_csv)
        if i_counter == 1: # Primera vez escribiendo en el csv, necesario crear el csv si no existe y header
            # CSV writer con header

            # Crear CSV vacío
            with open(file_name, 'w', newline='', encoding='utf-8') as archivo:
                # No escribir nada, archivo queda vacío
                pass

            csv_writer_tmax_todos_meses(file_name, i_idema, dicc_estacion_tmax ,header_bool = True)
        else:
            # CSV writer sin header
            csv_writer_tmax_todos_meses(file_name, i_idema, dicc_estacion_tmax, header_bool = False)