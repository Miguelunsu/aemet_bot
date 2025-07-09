import time
import os
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from fetch.extreme_values import get_extreme_values
from fetch.csv_reader import tmax_abs_reader, estacion_reader
from utils.comparer import abs_12h_comparer_tmax
from utils.csv_writer import csv_writer_tmax
from utils.parser import parser_temp_max
from utils.auxiliar import string_a_float_con_decimal

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("miapp.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.debug("Mensaje de debug")
logging.info("Mensaje informativo")
logging.warning("Advertencia")
logging.error("Error")
logging.critical("Error crítico")

def main():
    print(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        print("Iniciando main.", flush=True)

        # Calculo temperaturas extremas
        if False:
            i_counter = 0
            # Bucle temperaturas extremas
            for i_estacion in datos_estaciones:
                i_counter = i_counter + 1
                i_idema = i_estacion.get("idema")

                print(f"Estudiando Tmax en station: {idema}. Station {i_counter}/{len(datos_estaciones)}")
                print("Time sleep: 10")
                time.sleep(10)

                # Endpoint para valores extremos de temperatura
                endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{i_idema}'
                
                print(f"Llamando get_data_url_from_aemet (tempext). Estacion: {i_idema}", flush=True)
                data_url = get_data_url_from_aemet(endpoint)

                print(f"Estacion: {i_idema} -> data_url tempext: {data_url}", flush=True)
                data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo

                dicc_estacion_tmax = parser_temp_max(data)

                temMax = dicc_estacion_tmax.get("temMax")
                diaMax = dicc_estacion_tmax.get("diaMax")
                mesMax = dicc_estacion_tmax.get("mesMax")
                anioMax = dicc_estacion_tmax.get("anioMax")

                file_name = os.path.join(BASE_DIR, "tmax_estaciones.csv")
                if i_counter == 1:
                    # CSV writer con header
                    csv_writer_tmax(file_name, idema, temMax, diaMax, mesMax, anioMax, True)
                else:
                    # CSV writer sin header
                    csv_writer_tmax(file_name, idema, temMax, diaMax, mesMax, anioMax, False)

        # Obtención de medidas en tiempo real
        endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'
        print("Llamando get_data_url_from_aemet...", flush=True)

        data_url = get_data_url_from_aemet(endpoint)
        print(f"data_url: {data_url}", flush=True)

        print("Llamando download_data_from_url...", flush=True)
        data = download_data_from_url(data_url, retries=10) # Lista de diccionarios de estaciones meteo
        print(f"Datos descargados, cantidad: {len(data)}", flush=True)

        if isinstance(data, str) and data.lower() == "nan":
            raise ValueError("La variable es el string 'Nan'. No se ha podido conectar.")
        
        # Variable est_tmax_12h: Nested diccionary de estaciones con los datos de la temperatura maxima.
        est_tmax_12h = get_extreme_values(data, meteo_var="tamax")
        logging.info(f"Valores extremos obtenidos. Keys de est_tmax_12h: {list(est_tmax_12h.keys())}")

        # Reading a csv from tmax_estaciones_fijadas (maximos de temperaturas de estaciones)
        ruta_csv_tmax = os.path.join(BASE_DIR, "tmax_estaciones_fijadas.csv")
        
        # est_tmax_abs: diccionario con todas las temperaturas maximas.
        # Contiene idema, temMax, diaMax, mesMax, anioMax
        est_tmax_abs = tmax_abs_reader(ruta_csv_tmax)

        # para debugging y ver que los valores extremos se estan haciendo bien
        est_tmax_12h["0076"]["tamax"] = 77.7

        bool_est_extrem_12h = abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs)
        
        print("📈 Estaciones que superaron su T máxima:")
        for key, valores in bool_est_extrem_12h.items():
            if valores.get("Tmax_superada") is True:
                print(f"- {key}")

        # Leyendo datos de todas las estaciones
        ruta_csv_estaciones = os.path.join(BASE_DIR, "estaciones.csv")
        datos_estaciones = estacion_reader(ruta_csv_estaciones)

    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()