import time
import os
import sys

from fetch.csv_reader import tmax_reader_todays_month
from fetch.halfday_values import get_12h_values
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
        if True:
            
            # Leyendo datos de todas las estaciones y creando el csv tmax_estaciones.csv
            lectura_tmax_absolutas_aemet(BASE_DIR)

        # Obtención de medidas en tiempo real
        logging.info("Iniciando medidas en tiempo real")
        
        # est_tmax_12h: diccionario de máximos de temperatura para cada estacion en las ultimas 12h
        est_tmax_12h = get_12h_values()

        # Copiar el ultimo csv generado por lectura_tmax_absolutas_aemet
        # Nombrarlo "tmax_estaciones.csv" en la carpeta
        # tmax_estaciones.csv: maximos de temperaturas mes a mes de estaciones
        copiar_ultimo_csv_tmax(BASE_DIR, "tmax_estaciones")
        
        # Leer el csv de tmax_estaciones
        ruta_csv_tmax_mes_a_mes = os.path.join(BASE_DIR, "tmax_estaciones.csv")

        # mes actual en string como numero (ejemplo: agosto es "08")
        mes_actual_str_number = date.today().strftime('%m')
        
        # dic_est_tmax_mes: diccionario con las temperaturas máximas por estación (idema).
        # Cada entrada contiene temperatura, día y año del récord mensual. Claves: mes_target_temMax, mes_target_diaMax, mes_target_anioMax
        dic_est_tmax_mes = tmax_reader_todays_month(ruta_csv_tmax_mes_a_mes, mes_actual_str_number)

        # Para debugging y ver que los valores extremos se estan haciendo bien
        # est_tmax_12h["0009X"]["tamax"] = 88.8
        
        # bool_est_tmax_12h_superada: nested diccionario de bools: bool_est_extrem_12h, historic_day_tmax
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

        # encapsulado termin aqui: saber los maximos superados estas ultimas 12h

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