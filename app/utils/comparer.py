from utils.auxiliar import string_a_float_con_decimal
import logging
def abs_12h_comparer_tmax(est_tmax_12h, est_tmax_abs):
    # Compara el diccionario de 12h y abs para ver si se supera la tmax
    # est_tmax_12h: diccionario con las temperaturas maximas en las ultimas 12 horas
    # est_tmax_abs: diccionario con las temperaturas maximas históricas
    
    print("Funcion abs_12h_comparer iniciada")

    # Crear un nested diccionario de bools a partir de los datos de 12 horas, con las mismas keys (idemas)
    bool_est_extrem_12h = dict.fromkeys(est_tmax_12h)
    for key in est_tmax_12h.keys():
        bool_est_extrem_12h[key] = {
            "Tmax_superada": False,
            "Pluvmax_superada": False}

    # Bucle para ver si hay alguna estación en la que se ha superado la tmax
    for idema in est_tmax_12h:
        print(f"Evaluando idema para tmax: {idema}")

        # Extrayendo el string de tmax de 12h
        tmax_str = est_tmax_12h[idema]["tamax"]

        # Saltar si el valor actual no es válido
        if not tmax_str or str(tmax_str).lower() == "nan":
            print(f"⚠️ No se pudo convertir tamax a float para {idema}. Saltando...")
            continue

        # Comprobamos que no sea un string "NaN"
        try:
            tmax = float(tmax_str)
        except (ValueError, TypeError):
            print(f"⚠️ Valor inválido de tamax para {idema}: {tmax_str}. Saltando...")
            continue

        # Usamos .get(idema) para obtener el valor asociado a la clave 'idema' en est_tmax_abs
        # Esto comprueba automáticamente si la clave existe y evita un KeyError si no está
        # Si 'idema' no está presente, est_tmax_abs_info será None
        est_tmax_abs_info = est_tmax_abs.get(idema)
        # est_tmax_abs_info es un diccionario que contiene de este especifico idema.
        # Por ejemplo, para temepraturas: temMax,diaMax,mesMax,anioMax

        # Comprobamos que lo obtenido sea un diccionario válido. 
        if isinstance(est_tmax_abs_info, dict):

            # Intentamos obtener la clave "temMax" del subdiccionario.
            # Si no está, se devuelve None.
            temMax_abs_str = est_tmax_abs_info.get("temMax")

            # Esperamos un diccionario. Si no hay valor o es explícitamente un string "nan" → se ignora
            # Esta línea descarta valores vacíos, None, "", "nan", "NaN", etc.
            if not temMax_abs_str or (isinstance(temMax_abs_str, str) and temMax_abs_str.lower() == "nan"):
                print(f"⚠️ temMax histórica no válida para {idema}: {temMax_abs_str}. Saltando...")
                continue
            
            # Intentamos convertir el valor a float con función personalizada para pasar a decimal
            # Envolvemos en try/except por si la función lanza algún error inesperado
            try:
                temMax_abs = string_a_float_con_decimal(temMax_abs_str)
            except Exception as e:
                print(f"⚠️ Error convirtiendo temMax para {idema}: {e}")
                continue
            
            if temMax_abs is not None and tmax > temMax_abs:
                print(f"✅ T máxima superada en {idema}: actual {tmax} > histórica {temMax_abs}")
                bool_est_extrem_12h[idema]["Tmax_superada"] = True
        else:
            print(f"No se encontró una tmax para el idema {idema}")
    
    return bool_est_extrem_12h


def abs_12h_comparer_tmax_test(est_tmax_12h, est_tmax_abs):
    # Compara el diccionario de 12h y abs para ver si se supera la temp. maxima
    # est_tmax_12h: diccionario con las temperaturas maximas en las ultimas 12 horas
    # est_tmax_abs: diccionario con las temperaturas maximas históricas de ese mes
    
    print("Funcion abs_12h_comparer iniciada")

    # Crear un nested diccionario de bools a partir de los datos de 12 horas, con las mismas keys (idemas)
    bool_est_extrem_12h = dict.fromkeys(est_tmax_12h)
    for key in est_tmax_12h.keys():
        bool_est_extrem_12h[key] = {
            "Tmax_superada": False,
            "Pluvmax_superada": False}

    # Bucle para ver si hay alguna estación en la que se ha superado la tmax
    for idema in est_tmax_12h:
        logging.info(f"Evaluando si la temp de {idema} es la maxima del mes...")
        
        # Extrayendo el string de tmax de 12h AQUI EL tmax_str ES UN FLOAT, SE PUEDE CAMBIAR (EJEPLO 31.1)
        tamax_float = est_tmax_12h[idema]["tamax"]

        # Saltar si el valor actual no es válido
        if not tamax_float or str(tamax_float).lower() == "nan":
            logging.warning(f"No se pudo convertir tamax a float para {idema}. Saltando...")
            continue

        # Comprobamos que no sea un string "NaN"
        try:
            tamax_float = float(tamax_float)
        except (ValueError, TypeError):
            logging.warning(f"Valor inválido de tamax para {idema}: {tamax_float}. Saltando...")
            continue

        # Usamos .get(idema) para obtener el valor asociado a la clave 'idema' en est_tmax_abs
        # Esto comprueba automáticamente si la clave existe y evita un KeyError si no está
        # Si 'idema' no está presente, est_tmax_abs_info será None
        est_tmax_abs_info = est_tmax_abs.get(idema)
        # est_tmax_abs_info es un diccionario que contiene de este especifico idema.
        # Por ejemplo, para temepraturas: temMax,diaMax,mesMax,anioMax

        # Comprobamos que lo obtenido sea un diccionario válido. Ahora tendra claves "mes_target_temMax, mes_target_diaMax y mes_target_anioMax"
        if isinstance(est_tmax_abs_info, dict):

            # Intentamos obtener la clave "temMax" del subdiccionario.
            # Si no está, se devuelve None.
            temMax_abs = est_tmax_abs_info.get("mes_target_temMax")

            # Esperamos un diccionario. Si no hay valor o es explícitamente un string "nan" → se ignora
            # Esta línea descarta valores vacíos, None, "", "nan", "NaN", etc.
            if not temMax_abs or (isinstance(temMax_abs, str) and temMax_abs.lower() == "nan"):
                logging.warning(f"⚠️ temMax histórica no válida para {idema}: {temMax_abs}. Saltando...")
                continue
            
            if temMax_abs is not None and tamax_float > temMax_abs:
                logging.info(f"✅ T máxima superada en {idema}: actual {tamax_float} > histórica del mes {temMax_abs}")
                bool_est_extrem_12h[idema]["Tmax_superada"] = True
        else:
            logging.warning(f"No se encontró una tmax para el idema {idema}")
    
    return bool_est_extrem_12h