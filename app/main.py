import time
import os
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from fetch.extreme_values import get_extreme_values
from fetch.csv_reader import tmax_reader_todays_month
from utils.comparer import abs_12h_comparer_tmax
from utils.csv_manager import copiar_ultimo_csv_tmax
from fetch.extreme_csv_writer_from_aemet import lectura_tmax_absolutas_aemet
from utils.logger import configurar_logging
from datetime import date
import datetime
from bot.twitter_bot import post_tweet
import logging

def main():
    # Configurar logs
    configurar_logging()
    
    logging.info(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # try que encapsula todo el programa
    try:
        logging.info("Iniciando main.")

        # Lectura temperaturas extremas
        if False:
            
            # Leyendo datos de todas las estaciones y creando el csv tmax_estaciones.csv
            lectura_tmax_absolutas_aemet(BASE_DIR)

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
        
        # copiando el ultimo csv y nombrandolo "tmax_estaciones.csv"
        copiar_ultimo_csv_tmax(BASE_DIR, "tmax_estaciones")
        
        # Reading a csv from tmax_estaciones_fijadas (maximos de temperaturas mes a mes de estaciones)
        # ruta_csv_tmax_mes_a_mes: str enlace a csv con la info de maximas temp de estacion (mes a mes)
        ruta_csv_tmax_mes_a_mes = os.path.join(BASE_DIR, "tmax_estaciones.csv")

        mes_actual_str_number = date.today().strftime('%m')
        
        # est_tmax_mes_test: Diccionario con las temperaturas máximas por estación (idema).
        # Cada entrada contiene temperatura, día y año del récord mensual. Claves: mes_target_temMax, mes_target_diaMax, mes_target_anioMax
        # Los valores inválidos se retornan como None.
        dic_est_tmax_mes = tmax_reader_todays_month(ruta_csv_tmax_mes_a_mes, mes_actual_str_number)

        # Para debugging y ver que los valores extremos se estan haciendo bien
        # est_tmax_12h["0009X"]["tamax"] = 88.8
        
        # bool_est_extrem_12h = abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs)
        bool_est_tmax_12h_superada = abs_12h_comparer_tmax(est_tmax_12h, dic_est_tmax_mes)
    
        # keys que contienen los idemas que superaron la T max
        idemas_tmax_mes_superada = []
        print("Estaciones que superaron su T máxima:")
        for key, valores in bool_est_tmax_12h_superada[0].items():
            if valores.get("Tmax_superada_mes") is True:
                print(f"-> Superada para la estacion: {key}.")
                idemas_tmax_mes_superada.append(key)
                if valores.get("Tmax_superada_abs") is True:
                    print(f"!!! Superada de manera absoluta: {key}")
                    print(f"    Info del día de hoy{est_tmax_12h[key]}.")
                    print(f"    Info del día histórico{bool_est_tmax_12h_superada[1][key]}.")
                else:
                    print(f"    Info del día de hoy{est_tmax_12h[key]}.")
                    print(f"    Info del día histórico{bool_est_tmax_12h_superada[1][key]}.")

        print("Acabando programa")

        # Twittear
        # post_tweet("Bot funcionando con Tweepy Client y OAuth1 user context")
        # Marcar el periodo de refresco del cálculo de variables
        # periodo_horas = 12
        # periodo_segundos = periodo_horas*3600
        periodo_segundos = 10

        while True:
            # Cálculo de la hora actual
            current_time = datetime.datetime.now()
            logging.info(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] hey")

            # Ejecutar acción periódica

            # Esperar hasta el próximo intervalo
            time.sleep(periodo_segundos)

    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()