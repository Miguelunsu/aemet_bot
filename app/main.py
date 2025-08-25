import time
import os
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from fetch.extreme_values import get_extreme_values
from fetch.csv_reader import estacion_reader, tmax_reader_todays_month
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

# EJEMPLOS DE LOGS
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
                
                dicc_estacion_tmax2 = parser_temp_max_todos_meses(data)
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
                    csv_writer_tmax_todos_meses(file_name, i_idema, dicc_estacion_tmax2 ,header_bool = True)
                else:
                    # CSV writer sin header
                    csv_writer_tmax_todos_meses(file_name, i_idema, dicc_estacion_tmax2, header_bool = False)


        # Obtención de medidas en tiempo real
        logging.info("Iniciando medidas en tiempo real")

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
        
        # est_tmax_12h: nested diccionary de estaciones con los datos de la temperatura maxima. El dicc. contiene fint (hora), tamax, ubi, lat y lon
        est_tmax_12h = get_extreme_values(data, meteo_var="tamax")
        logging.info(f"Valores extremos de T obtenidos. Número de estaciones encontradas: {len(est_tmax_12h.keys())}")
        # Reading a csv from tmax_estaciones_fijadas (maximos de temperaturas mes a mes de estaciones)
        # ruta_csv_tmax_mes_a_mes: str enlace a csv con la info de maximas temp de estacion (mes a mes)
        ruta_csv_tmax_mes_a_mes = os.path.join(BASE_DIR, "tmax_estaciones_mes_a_mes_fijadas.csv")

        mes_actual_str_number = date.today().strftime('%m')
        
        # est_tmax_mes_test: Diccionario con las temperaturas máximas por estación (idema).
        # Cada entrada contiene temperatura, día y año del récord mensual. Claves: mes_target_temMax, mes_target_diaMax, mes_target_anioMax
        # Los valores inválidos se retornan como None.
        dic_est_tmax_mes = tmax_reader_todays_month(ruta_csv_tmax_mes_a_mes, mes_actual_str_number)

        # para debugging y ver que los valores extremos se estan haciendo bien
        est_tmax_12h["0009X"]["tamax"] = 88.8
        
        # bool_est_extrem_12h = abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs)
        bool_est_tmax_12h_superada = abs_12h_comparer_tmax_test(est_tmax_12h, dic_est_tmax_mes)

        print("Estaciones que superaron su T máxima:")
        for key, valores in bool_est_tmax_12h_superada.items():
            if valores.get("Tmax_superada") is True:
                print(f"- {key}")


    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()