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
from bot.twitter_bot import post_tweet, scheduler, create_tweet
import logging
from datetime import datetime

def lecutura_extremos_actualizar_csvs(BASE_DIR):
    # Leyendo datos de todas las estaciones (temp y pluv) y actualiza los csvs
    
    lectura_absolutas_aemet(BASE_DIR)

    # Copiar el ultimo csv generado por lectura_absolutas_aemet
    actualizar_csv(BASE_DIR, "tmax_estaciones")
    actualizar_csv(BASE_DIR, "pluvmax_estaciones")

def get_records_data(BASE_DIR):
    # Obtiene la info de los records
    
    try:
        logging.info("Iniciando main.")

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

        # Ajuste de unidades extremas vs 12h
        # Para temp: en extremas: xxx
        #            en 12h, xxx
        # Para prec: en extremas: decimas de mm
        #            en 12h, mm
        if True:
            for idema in records_temp_estaciones.keys():
                # temp
                if records_temp_estaciones[idema]["mensual_valor"] is not None:
                    records_temp_estaciones[idema]["mensual_valor"] = records_temp_estaciones[idema]["mensual_valor"]*0.1
                if records_temp_estaciones[idema]["absoluto_valor"] is not None:   
                    records_temp_estaciones[idema]["absoluto_valor"] = records_temp_estaciones[idema]["absoluto_valor"]*0.1
                # prec
                if records_pluv_estaciones[idema]["mensual_valor"] is not None:
                    records_pluv_estaciones[idema]["mensual_valor"] = records_pluv_estaciones[idema]["mensual_valor"]*0.1
                if records_pluv_estaciones[idema]["absoluto_valor"] is not None:   
                    records_pluv_estaciones[idema]["absoluto_valor"] = records_pluv_estaciones[idema]["absoluto_valor"]*0.1

        # Bools que guardan los records
        records_superados_temp_bool, previous_record_temp_info = check_record_breaks(max_temp_12h_estaciones, records_temp_estaciones)
        records_superados_pluv_bool, previous_record_pluv_info = check_record_breaks(sum_pluv_12h_estaciones, records_pluv_estaciones)
    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

    return (
        records_superados_temp_bool,
        previous_record_temp_info,
        max_temp_12h_estaciones,
        records_superados_pluv_bool,
        previous_record_pluv_info,
        sum_pluv_12h_estaciones
    )

def main():
    # Configurar logs
    configurar_logging()
    
    logging.info(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Actualizar los csvs
    if False:
        lecutura_extremos_actualizar_csvs()

    # Encontrar los records
    if True:
        # Obteniendo los bools de los records
        (
            records_superados_temp_bool,
            previous_record_temp_info,
            max_temp_12h_estaciones,
            records_superados_pluv_bool,
            previous_record_pluv_info,
            sum_pluv_12h_estaciones
        ) = get_records_data(BASE_DIR)

    # showcase de los records
    if True:
        # keys que contienen los idemas que superaron la T max
        idemas_tmax_mes_superada = []
        logging.info("Estaciones que superaron su T máxima:")
        for key, valores in records_superados_temp_bool.items():
            if valores.get("valor_superado_mes") is True:
                idemas_tmax_mes_superada.append(key)
                if valores.get("valor_superado_abs") is True:
                    logging.info(f"-> Superada la ABSOLUTA: {key}")
                    logging.info(f"Día de hoy{max_temp_12h_estaciones[key]}.")
                    logging.info(f"Día histórico{previous_record_temp_info[key]}.")

                    tweet_text = create_tweet(max_temp_12h_estaciones[key],
                                 previous_record_temp_info[key],
                                 key,
                                 "temp_max",
                                 BASE_DIR)
                    post_tweet(tweet_text)
                else:
                    logging.info(f"-> Superada la MENSUAL la estacion: {key}.")
                    logging.info(f"Día de hoy{max_temp_12h_estaciones[key]}.")
                    logging.info(f"Día histórico{previous_record_temp_info[key]}.")

                    tweet_text = create_tweet(max_temp_12h_estaciones[key],
                                 previous_record_temp_info[key],
                                 key,
                                 "temp_max",
                                 BASE_DIR)
                    post_tweet(tweet_text)

        logging.info("Estaciones que superaron su prec máxima:")
        for key, valores in records_superados_pluv_bool.items():
            if valores.get("valor_superado_mes") is True:
                idemas_tmax_mes_superada.append(key)
                if valores.get("valor_superado_abs") is True:
                    logging.info(f"-> Superada la ABSOLUTA: {key}")
                    logging.info(f"Día de hoy{sum_pluv_12h_estaciones[key]}.")
                    logging.info(f"Día histórico{previous_record_pluv_info[key]}.")
                else:
                    logging.info(f"-> Superada la MENSUAL la estacion: {key}.")
                    logging.info(f"Día de hoy{sum_pluv_12h_estaciones[key]}.")
                    logging.info(f"Día histórico{previous_record_pluv_info[key]}.")

    # schudeler
    # scheduler(horas=["22:40","22:44"])
    
if __name__ == "__main__":
    main()