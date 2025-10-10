from utils.auxiliar import string_a_float_con_decimal
import logging
from datetime import date

def check_record_breaks(max_value_12h_estaciones, redords_estaciones):
    # Compara el diccionario de 12h y abs para ver si se supera la value. maxima
    # max_value_12h_estaciones: diccionario con las valueeraturas maximas en las ultimas 12 value
    # redords_estaciones: diccionario con las valueeraturas maximas históricas de ese mes y absolutas
    
    # Devuelve un set de bools que indican los records
    # Nested diccionario de bools
    records_superados_bool = {}
    previous_record_info = {}
    for key in max_value_12h_estaciones.keys():
        records_superados_bool[key] = {
            "valor_superado_mes": False,
            "valor_superado_abs": False}
        previous_record_info[key] = {False}
        
    # Bucle para ver si hay alguna estación en la que se ha superado la tmax
    for idema in max_value_12h_estaciones:     
        # Extrayendo el string de tmax de 12h AQUI EL tmax_str ES UN FLOAT, SE PUEDE CAMBIAR (EJEPLO 31.1)
        ole = max_value_12h_estaciones[idema]
        value_float = max_value_12h_estaciones[idema]["value"]
        if idema == "7012C":
            pass
        # Comprobamos que no sea un string "NaN"
        try:
            value_float = float(value_float)
        except (ValueError, TypeError):
            logging.warning(f"Valor inválido de value para {idema}: {value_float}. Saltando...")
            continue

        # Usamos .get(idema) para obtener el valor asociado a la clave 'idema' en redords_estaciones
        # Esto comprueba automáticamente si la clave existe y evita un KeyError si no está
        # Si 'idema' no está presente, redord_idema será None
        redord_idema = redords_estaciones.get(idema)
        # redord_idema es un diccionario que contiene de este especifico idema.
        # Por ejemplo, para temepraturas: temMax,diaMax,mesMax,anioMax

        # Comprobamos que lo obtenido sea un diccionario válido. Ahora tendra claves
        # "mes_target_temMax, mes_target_diaMax, mes_target_anioMax"
        # 'abs_value', 'abs_dia', 'abs_mes', 'abs_anio'
        if isinstance(redord_idema, dict):

            # Intentamos obtener la clave "temMax" del subdiccionario.
            # Si no está, se devuelve None.
            valor_record_mensual = redord_idema.get("mensual_valor")
            valor_record_absoluto = redord_idema.get("absoluto_valor")

            # Esperamos un diccionario.
            # Esta línea descarta valores vacíos, None, "", "nan", "NaN", etc.
            if not valor_record_mensual or (isinstance(valor_record_mensual, str) and valor_record_mensual.lower() == "nan"):
                logging.warning(f"⚠️ temMax histórica no válida para {idema}: {valor_record_mensual}. Saltando...")
                continue
            
            if valor_record_mensual is not None and value_float > valor_record_mensual:
                records_superados_bool[idema]["valor_superado_mes"] = True
                
                previous_record_info[idema] = {
                    "dia": redord_idema.get("mensual_dia"),
                    "mes": date.today().strftime('%m'),
                    "anio": redord_idema.get("mensual_anio"),
                    "value": valor_record_mensual
                }
                logging.info(f"T máxima del mes superada en {idema}: actual {value_float} > histórica del mes {valor_record_mensual}")
                # logging.info(f"Info del día del mes con valueeratura max anterior: {previous_record_info}")
                # Ahora obtenemos la mas alta absoluta
                # valor_record_mensual = redord_idema.get("mes_target_temMax")
                if valor_record_absoluto is not None and value_float > valor_record_absoluto:
                    records_superados_bool[idema]["valor_superado_abs"] = True
                    previous_record_info[idema] = {
                        "dia": redord_idema.get("absoluto_dia"),
                        "mes": redord_idema.get("absoluto_mes"),
                        "anio": redord_idema.get("absoluto_anio"),
                        "value": valor_record_absoluto
                    }

                    logging.info(f"T máxima absoluta superada en {idema}: actual {value_float} > histórica del mes {valor_record_absoluto}")
                    # logging.info(f"Info del día del mes con valueeratura max anterior: {previous_record_info}")
            else:
                logging.info(f"T máxima NO superada en {idema}: actual {value_float} > histórica del mes {valor_record_mensual}")
        else:
            logging.warning(f"No se encontró una tmax para el idema {idema}")
    
    return [records_superados_bool, previous_record_info]