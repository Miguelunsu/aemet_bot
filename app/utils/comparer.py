from utils.auxiliar import string_a_float_con_decimal
import logging
from datetime import date

def abs_12h_comparer_tmax(max_temp_12h_estaciones, datos_temp_estaciones):
    # Compara el diccionario de 12h y abs para ver si se supera la temp. maxima
    # max_temp_12h_estaciones: diccionario con las temperaturas maximas en las ultimas 12 horas
    # datos_temp_estaciones: diccionario con las temperaturas maximas históricas de ese mes y absolutas
    
    # Crear un nested diccionario de bools a partir de los datos de 12 horas, con las mismas keys (idemas)
    # Tambien el diccionario que tiene el dia anterior de la tmax
    bool_est_extrem_12h = dict.fromkeys(max_temp_12h_estaciones)
    historic_day_tmax = dict.fromkeys(max_temp_12h_estaciones)

    for key in max_temp_12h_estaciones.keys():
        bool_est_extrem_12h[key] = {
            "Tmax_superada_mes": False,
            "Tmax_superada_abs": False}
        historic_day_tmax[key] = {False}
        
    # Bucle para ver si hay alguna estación en la que se ha superado la tmax
    for idema in max_temp_12h_estaciones:     
        # Extrayendo el string de tmax de 12h AQUI EL tmax_str ES UN FLOAT, SE PUEDE CAMBIAR (EJEPLO 31.1)
        tamax_float = max_temp_12h_estaciones[idema]["tamax"]

        # Comprobamos que no sea un string "NaN"
        try:
            tamax_float = float(tamax_float)
        except (ValueError, TypeError):
            logging.warning(f"Valor inválido de tamax para {idema}: {tamax_float}. Saltando...")
            continue

        # Usamos .get(idema) para obtener el valor asociado a la clave 'idema' en datos_temp_estaciones
        # Esto comprueba automáticamente si la clave existe y evita un KeyError si no está
        # Si 'idema' no está presente, datos_temp_idema será None
        datos_temp_idema = datos_temp_estaciones.get(idema)
        # datos_temp_idema es un diccionario que contiene de este especifico idema.
        # Por ejemplo, para temepraturas: temMax,diaMax,mesMax,anioMax

        # Comprobamos que lo obtenido sea un diccionario válido. Ahora tendra claves
        # "mes_target_temMax, mes_target_diaMax, mes_target_anioMax"
        # 'abs_temp', 'abs_dia', 'abs_mes', 'abs_anio'
        if isinstance(datos_temp_idema, dict):

            # Intentamos obtener la clave "temMax" del subdiccionario.
            # Si no está, se devuelve None.
            mensual_valor = datos_temp_idema.get("mensual_valor")
            absoluto_valor = datos_temp_idema.get("absoluto_valor")

            # Esperamos un diccionario.
            # Esta línea descarta valores vacíos, None, "", "nan", "NaN", etc.
            if not mensual_valor or (isinstance(mensual_valor, str) and mensual_valor.lower() == "nan"):
                logging.warning(f"⚠️ temMax histórica no válida para {idema}: {mensual_valor}. Saltando...")
                continue
            
            if mensual_valor is not None and tamax_float > mensual_valor:
                bool_est_extrem_12h[idema]["Tmax_superada_mes"] = True
                
                historic_day_tmax[idema] = {
                    "dia": datos_temp_idema.get("mes_target_diaMax"),
                    "mes": date.today().strftime('%m'),
                    "anio": datos_temp_idema.get("mes_target_anioMax"),
                    "temp": mensual_valor
                }
                logging.info(f"T máxima del mes superada en {idema}: actual {tamax_float} > histórica del mes {mensual_valor}")
                logging.info(f"Info del día del mes con temperatura max anterior: {historic_day_tmax}")
                # Ahora obtenemos la mas alta absoluta
                # mensual_valor = datos_temp_idema.get("mes_target_temMax")
                if tamax_float > absoluto_valor:
                    bool_est_extrem_12h[idema]["Tmax_superada_abs"] = True
                    historic_day_tmax[idema] = {
                        "dia": datos_temp_idema.get("abs_dia"),
                        "mes": datos_temp_idema.get("abs_mes"),
                        "anio": datos_temp_idema.get("abs_anio"),
                        "temp": absoluto_valor
                    }

                    logging.info(f"T máxima absoluta superada en {idema}: actual {tamax_float} > histórica del mes {absoluto_valor}")
                    logging.info(f"Info del día del mes con temperatura max anterior: {historic_day_tmax}")
            else:
                logging.info(f"T máxima NO superada en {idema}: actual {tamax_float} > histórica del mes {mensual_valor}")
        else:
            logging.warning(f"No se encontró una tmax para el idema {idema}")
    
    return [bool_est_extrem_12h, historic_day_tmax]