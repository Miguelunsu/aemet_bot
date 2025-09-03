from utils.auxiliar import string_a_float_con_decimal
import logging
from datetime import date

def abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs):
    # Compara el diccionario de 12h y abs para ver si se supera la temp. maxima
    # est_tmax_12h: diccionario con las temperaturas maximas en las ultimas 12 horas
    # est_tmax_abs: diccionario con las temperaturas maximas históricas de ese mes
    
    # Crear un nested diccionario de bools a partir de los datos de 12 horas, con las mismas keys (idemas)
    # Tambien el diccionario que tiene el dia anterior de la tmax
    bool_est_extrem_12h = dict.fromkeys(est_tmax_12h)
    historic_day_tmax = dict.fromkeys(est_tmax_12h)

    for key in est_tmax_12h.keys():
        bool_est_extrem_12h[key] = {
            "Tmax_superada_mes": False,
            "Tmax_superada_abs": False}
        historic_day_tmax[key] = {False}
        
    # Bucle para ver si hay alguna estación en la que se ha superado la tmax
    for idema in est_tmax_12h:     
        # Extrayendo el string de tmax de 12h AQUI EL tmax_str ES UN FLOAT, SE PUEDE CAMBIAR (EJEPLO 31.1)
        tamax_float = est_tmax_12h[idema]["tamax"]

        # Comprobamos que no sea un string "NaN"
        try:
            tamax_float = float(tamax_float)
        except (ValueError, TypeError):
            logging.warning(f"Valor inválido de tamax para {idema}: {tamax_float}. Saltando...")
            continue

        # Usamos .get(idema) para obtener el valor asociado a la clave 'idema' en est_tmax_abs
        # Esto comprueba automáticamente si la clave existe y evita un KeyError si no está
        # Si 'idema' no está presente, dic_tmax_mes_abs_idema será None
        dic_tmax_mes_abs_idema = est_tmax_abs.get(idema)
        # dic_tmax_mes_abs_idema es un diccionario que contiene de este especifico idema.
        # Por ejemplo, para temepraturas: temMax,diaMax,mesMax,anioMax

        # Comprobamos que lo obtenido sea un diccionario válido. Ahora tendra claves
        # "mes_target_temMax, mes_target_diaMax, mes_target_anioMax"
        # 'abs_temp', 'abs_dia', 'abs_mes', 'abs_anio'
        if isinstance(dic_tmax_mes_abs_idema, dict):

            # Intentamos obtener la clave "temMax" del subdiccionario.
            # Si no está, se devuelve None.
            temMax_mes = dic_tmax_mes_abs_idema.get("mes_target_temMax")
            temMax_abs = dic_tmax_mes_abs_idema.get("abs_temp")

            # Esperamos un diccionario. Si no hay valor o es explícitamente un string "nan" → se ignora
            # Esta línea descarta valores vacíos, None, "", "nan", "NaN", etc.
            if not temMax_mes or (isinstance(temMax_mes, str) and temMax_mes.lower() == "nan"):
                logging.warning(f"⚠️ temMax histórica no válida para {idema}: {temMax_mes}. Saltando...")
                continue
            
            if temMax_mes is not None and tamax_float > temMax_mes:
                bool_est_extrem_12h[idema]["Tmax_superada_mes"] = True
                
                historic_day_tmax[idema] = {
                    "dia": dic_tmax_mes_abs_idema.get("mes_target_diaMax"),
                    "mes": date.today().strftime('%m'),
                    "anio": dic_tmax_mes_abs_idema.get("mes_target_anioMax"),
                    "temp": temMax_mes
                }
                logging.info(f"T máxima del mes superada en {idema}: actual {tamax_float} > histórica del mes {temMax_mes}")
                logging.info(f"Info del día del mes con temperatura max anterior: {historic_day_tmax}")
                # Ahora obtenemos la mas alta absoluta
                # temMax_mes = dic_tmax_mes_abs_idema.get("mes_target_temMax")
                if tamax_float > temMax_abs:
                    bool_est_extrem_12h[idema]["Tmax_superada_abs"] = True
                    historic_day_tmax[idema] = {
                        "dia": dic_tmax_mes_abs_idema.get("abs_dia"),
                        "mes": dic_tmax_mes_abs_idema.get("abs_mes"),
                        "anio": dic_tmax_mes_abs_idema.get("abs_anio"),
                        "temp": temMax_abs
                    }

                    logging.info(f"T máxima absoluta superada en {idema}: actual {tamax_float} > histórica del mes {temMax_abs}")
                    logging.info(f"Info del día del mes con temperatura max anterior: {historic_day_tmax}")
            else:
                logging.info(f"T máxima NO superada en {idema}: actual {tamax_float} > histórica del mes {temMax_mes}")
        else:
            logging.warning(f"No se encontró una tmax para el idema {idema}")
    
    return [bool_est_extrem_12h, historic_day_tmax]