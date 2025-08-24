import time
import os
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from fetch.extreme_values import get_extreme_values
from fetch.csv_reader import tmax_abs_reader, estacion_reader, tmax_reader_todays_month
from utils.comparer import abs_12h_comparer_tmax, abs_12h_comparer_tmax_test
from utils.csv_writer import csv_writer_tmax, csv_writer_tmax_todos_meses
from utils.parser import parser_temp_max, parser_temp_max_todos_meses
from datetime import date

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

#logging.debug("Mensaje de debug")
#logging.info("Mensaje informativo")
#logging.warning("Advertencia")
#logging.error("Error")
#logging.critical("Error crítico")

def main():
    logging.info(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        logging.info("Iniciando main.")

        # Calculo temperaturas extremas
        if False:
            
            # Leyendo datos de todas las estaciones
            ruta_csv_estaciones = os.path.join(BASE_DIR, "estaciones.csv")
            datos_estaciones = estacion_reader(ruta_csv_estaciones)

            i_counter = 0
            # Bucle temperaturas extremas
            for i_estacion in datos_estaciones:
                i_counter = i_counter + 1
                i_idema = i_estacion.get("idema")

                logging.info(f"Estudiando Tmax en station: {i_idema}. Station {i_counter}/{len(datos_estaciones)}")
                logging.info("Time sleep: 10")
                time.sleep(10)

                # Endpoint para valores extremos de temperatura
                endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{i_idema}'
                data_url = get_data_url_from_aemet(endpoint)

                logging.info(f"Estacion: {i_idema} -> data_url tempext: {data_url}")
                data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
                
                data2 = data
                if data == "Nan":
                    pass

                dicc_estacion_tmax = parser_temp_max(data)
                dicc_estacion_tmax2 = parser_temp_max_todos_meses(data2)
                """
                dicc_estacion_tmax2
                Diccionario con la siguiente estructura:
                {
                    "idema": str,
                    "ene_temp": str, "ene_dia": str, "ene_anio": str,
                    "feb_temp": ..., "feb_dia": ..., "feb_anio": ...,
                    ...
                    "dic_temp": ..., "dic_dia": ..., "dic_anio": ...
                }
                """
                file_name = os.path.join(BASE_DIR, "tmax_estaciones_test.csv")
                if i_counter == 1: # Primera vez escribiendo en el csv, necesario header
                    csv_writer_tmax_todos_meses (file_name, i_idema, dicc_estacion_tmax2 ,header_bool = True)
                else:
                    # CSV writer sin header
                    csv_writer_tmax_todos_meses(file_name, i_idema, dicc_estacion_tmax2, header_bool = False)

                temMax = dicc_estacion_tmax.get("temMax")
                diaMax = dicc_estacion_tmax.get("diaMax")
                mesMax = dicc_estacion_tmax.get("mesMax")
                anioMax = dicc_estacion_tmax.get("anioMax")

                file_name = os.path.join(BASE_DIR, "tmax_estaciones.csv")
                if i_counter == 1:
                    # CSV writer con header
                    csv_writer_tmax(file_name, i_idema, temMax, diaMax, mesMax, anioMax, True)
                else:
                    # CSV writer sin header
                    csv_writer_tmax(file_name, i_idema, temMax, diaMax, mesMax, anioMax, False)

        # Obtención de medidas en tiempo real
        logging.info("Iniciando medidas en tiempo real")

        endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'

        data_url = get_data_url_from_aemet(endpoint)

        data = download_data_from_url(data_url, retries=10) # Lista de diccionarios de estaciones meteo
        print(f"Datos descargados, cantidad: {len(data)}", flush=True)

        if isinstance(data, str) and data.lower() == "nan":
            raise ValueError("La variable es el string 'Nan'. No se ha podido conectar.")
        
        # Variable est_tmax_12h: Nested diccionary de estaciones con los datos de la temperatura maxima.
        est_tmax_12h = get_extreme_values(data, meteo_var="tamax")
        logging.info(f"Valores extremos de T obtenidos. Número de estaciones encontradas: {len(est_tmax_12h.keys())}")

        # Reading a csv from tmax_estaciones_fijadas (maximos de temperaturas de estaciones)
        ruta_csv_tmax = os.path.join(BASE_DIR, "tmax_estaciones_fijadas.csv")
        # Testing para las temperaturas mes a mes
        ruta_csv_tmax_test = os.path.join(BASE_DIR, "tmax_estaciones_test_fijadas.csv")

        # est_tmax_abs: diccionario con todas las temperaturas maximas.
        # Contiene idema, temMax, diaMax, mesMax, anioMax
        est_tmax_abs = tmax_abs_reader(ruta_csv_tmax)
        
        # Testing
        # Obteniendo el mes de hoy
        mes_actual_str_number = date.today().strftime('%m')
        est_tmax_abs_test = tmax_reader_todays_month(ruta_csv_tmax_test, mes_actual_str_number)

        # para debugging y ver que los valores extremos se estan haciendo bien
        est_tmax_12h["0009X"]["tamax"] = 88.8
        
        # bool_est_extrem_12h = abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs)
        bool_est_extrem_12h_test = abs_12h_comparer_tmax_test(est_tmax_12h, est_tmax_abs_test)

        print("📈 Estaciones que superaron su T máxima:")
        for key, valores in bool_est_extrem_12h_test.items():
            if valores.get("Tmax_superada") is True:
                print(f"- {key}")


    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()