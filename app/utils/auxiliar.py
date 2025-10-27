import logging
import os
from datetime import date
from datetime import datetime
import time
import math

from fetch.csv_reader import get_max_values_current_month
from fetch.halfday_values import get_12h_values
from utils.comparer import check_record_breaks
from bot.twitter_bot import tweet_manager
from utils.prec_cummulative import guardar_valores_en_csv, leer_csv_a_diccionario, borrar_csv

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
        logging.info("Leyendo records: temp")
        records_superados_temp_bool, previous_record_temp_info = check_record_breaks(max_temp_12h_estaciones, records_temp_estaciones)
        logging.info("Leyendo records: pluv")
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

def scheduler(BASE_DIR,
              horas=["23:00","12:00"]):
    # Función disparador para las horas
    
    # diccionario que le da a cada hora un False
    ejecutado_hoy = dict.fromkeys(horas, False)

    while True:
        ahora = datetime.now()
        hora_actual = f"{ahora.hour:02d}:{ahora.minute:02d}" # formato 00:10

        logging.info(f"Bucle de scheduler. Hora actual: {hora_actual}. Horas a comparar: {list(ejecutado_hoy.keys())}")
        # Comprobar cada hora objetivo
        for objetivo in ejecutado_hoy:
            
            if hora_actual == objetivo and not ejecutado_hoy[objetivo]:
                logging.info(f"Hora del bucle activada: {objetivo}.")

                # Obteniendo los bools de los records
                (
                    records_superados_temp_bool,
                    previous_record_temp_info,
                    max_temp_12h_estaciones,
                    records_superados_pluv_bool,
                    previous_record_pluv_info,
                    sum_pluv_12h_estaciones
                ) = get_records_data(BASE_DIR)
                
                if hora_actual == horas[0]: # primera hora: guardamos csv. Seguimos como si nada.
                    guardar_valores_en_csv(sum_pluv_12h_estaciones)
                elif hora_actual == horas[-1]: # ultima hora: recogemos lo del csv y lo sumamos. Es el cumulativo del dia
                    datos_previos = leer_csv_a_diccionario()
                    # Se hace la suma
                    for idema, valor in datos_previos.items():
                        try:
                            valor = float(valor)
                            if not math.isnan(valor):
                                sum_pluv_12h_estaciones[idema]["value"] = sum_pluv_12h_estaciones[idema]["value"] + valor
                        except (TypeError, ValueError):
                            pass
                    # se borra el contenido del csv
                    borrar_csv()
                else:
                    pass

                # Hacer todo el proceso de los tweets:
                tweet_manager(  records_superados_temp_bool,
                                previous_record_temp_info,
                                max_temp_12h_estaciones,
                                records_superados_pluv_bool,
                                previous_record_pluv_info,
                                sum_pluv_12h_estaciones,
                                hora_actual,
                                BASE_DIR)
                
                # Se ha ejecutado a esta hora
                ejecutado_hoy[objetivo] = True

        time.sleep(30)  # Espera 30 segundos antes de volver a comprobar