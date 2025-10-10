import time
import os
import sys

from fetch.csv_reader import get_max_values_current_month
from fetch.halfday_values import get_12h_values
from utils.comparer import check_record_breaks
from utils.csv_manager import actualizar_csv
from fetch.extreme_csv_writer_from_aemet import lectura_absolutas_aemet
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
            lectura_absolutas_aemet(BASE_DIR)

            # Copiar el ultimo csv generado por lectura_absolutas_aemet
            actualizar_csv(BASE_DIR, "tmax_estaciones")
            actualizar_csv(BASE_DIR, "pluvmax_estaciones")

        # Obtención de medidas en tiempo real
        logging.info("Iniciando medidas en tiempo real")
        # max_temp_12h_estaciones: diccionario de máximos de temperatura para cada estacion en las ultimas 12h
        max_temp_12h_estaciones = get_12h_values(meteo_var="tamax")
        # sum_pluv_12h_estaciones: diccionario de sumatorios de lluvia para cada estacion en las ultimas 12h
        sum_pluv_12h_estaciones = get_12h_values(meteo_var="prec")

        # Leer el csv de tmax_estaciones y pluv
        ruta_csv_tmax_mes_a_mes = os.path.join(BASE_DIR, "tmax_estaciones.csv")
        ruta_csv_pluvmax_mes_a_mes = os.path.join(BASE_DIR, "pluvmax_estaciones.csv")

        # mes actual en string como numero (ejemplo: agosto es "08")
        mes_actual_str_number = date.today().strftime('%m')
        
        # datos_temp_estaciones: diccionario con las temperaturas máximas por estación (idema).
            # Cada entrada contiene temperatura, día y año del récord mensual. Claves:
            # mensual_valor, mensual_dia, mensual_anio
            # absoluto_valor, absoluto_dia, absoluto_mes, absoluto_anio
        records_temp_estaciones = get_max_values_current_month(ruta_csv_tmax_mes_a_mes, mes_actual_str_number)
        records_pluv_estaciones = get_max_values_current_month(ruta_csv_pluvmax_mes_a_mes, mes_actual_str_number)

        # Ajuste temperaturas max del csv
        if True:
            for idema in records_temp_estaciones.keys():
                if records_temp_estaciones[idema]["mensual_valor"] is not None:
                    records_temp_estaciones[idema]["mensual_valor"] = records_temp_estaciones[idema]["mensual_valor"]*0.1
                if records_temp_estaciones[idema]["absoluto_valor"] is not None:   
                    records_temp_estaciones[idema]["absoluto_valor"] = records_temp_estaciones[idema]["absoluto_valor"]*0.1
       
        # records_superados_temp_bool: nested diccionario de bools: valor_superado_mes, valor_superado_abs
        # records_superados_temp_bool, previous_record_temp_info = check_record_breaks(max_temp_12h_estaciones, datos_temp_estaciones)
        records_superados_temp_bool, previous_record_temp_info = check_record_breaks(max_temp_12h_estaciones, records_temp_estaciones)
        records_superados_pluv_bool, previous_record_pluv_info = check_record_breaks(sum_pluv_12h_estaciones, records_pluv_estaciones)

        # keys que contienen los idemas que superaron la T max
        idemas_tmax_mes_superada = []
        print("Estaciones que superaron su T máxima:")
        for key, valores in records_superados_temp_bool.items():
            if valores.get("valor_superado_mes") is True:
                print(f"-> Superada para la estacion: {key}.")
                idemas_tmax_mes_superada.append(key)
                if valores.get("valor_superado_abs") is True:
                    print(f"!!! Superada de manera absoluta: {key}")
                    print(f"    Info del día de hoy{max_temp_12h_estaciones[key]}.")
                    print(f"    Info del día histórico{previous_record_temp_info[key]}.")
                else:
                    print(f"    Info del día de hoy{max_temp_12h_estaciones[key]}.")
                    print(f"    Info del día histórico{previous_record_temp_info[key]}.")

        print("Estaciones que superaron su prec máxima:")
        for key, valores in records_superados_pluv_bool.items():
            if valores.get("valor_superado_mes") is True:
                print(f"-> Superada para la estacion: {key}.")
                idemas_tmax_mes_superada.append(key)
                if valores.get("valor_superado_abs") is True:
                    print(f"!!! Superada de manera absoluta: {key}")
                    print(f"    Info del día de hoy{sum_pluv_12h_estaciones[key]}.")
                    print(f"    Info del día histórico{previous_record_pluv_info[key]}.")
                else:
                    print(f"    Info del día de hoy{sum_pluv_12h_estaciones[key]}.")
                    print(f"    Info del día histórico{previous_record_pluv_info[key]}.")
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