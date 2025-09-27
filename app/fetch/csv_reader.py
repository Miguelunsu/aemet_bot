import csv
import logging

def tmax_abs_reader(ruta_tmax_abs_csv):
    print(f"Leyendo las tmax abs del csv {ruta_tmax_abs_csv}")
    est_tmax_abs = {} # diccionario con todas las temperaturas maximas. Contiene idema, temMax, diaMax, mesMax, anioMax

    with open(ruta_tmax_abs_csv, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            est_tmax_abs[fila['idema']] = {
                'temMax': fila['temMax'],
                'diaMax': float(fila['diaMax']),
                'mesMax': float(fila['mesMax']),
                'anioMax': float(fila['anioMax'])
                }
    print("Datos de tem max leidos del csv.")
    return est_tmax_abs

def estacion_reader(ruta_csv_estaciones):
    datos_estaciones = []

    with open(ruta_csv_estaciones, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            datos_estaciones.append({
                'idema': fila['idema'],
                'ubi': fila['ubi'],
                'lon': float(fila['lon']),
                'lat': float(fila['lat'])
            })
    return datos_estaciones

def es_valor_valido(valor):
    """Verifica si un valor es numérico y válido"""
    try:
        if valor is None or str(valor).strip().lower() in ['', 'nan', 'null', 'none']:
            return False
        float(valor)
        return True
    except (ValueError, TypeError):
        return False

def tmax_reader_todays_month(ruta_tmax_abs_csv, mes_actual_str_number):
    """
    Lee las temperaturas máximas absolutas del mes actual desde un archivo CSV.
    
    Args:
        ruta_tmax_abs_csv (str): Ruta del archivo CSV con los datos de temperaturas maximas
        mes_actual_str_number (str): Número del mes en formato '01' a '12'
    
    Returns:
        dic_datos_estaciones: 	Diccionario con las temperaturas máximas por estación (idema).
								Cada entrada contiene temperatura, día y año del récord mensual.
								Los valores inválidos se retornan como None.
    
    Example:
        >>> datos = tmax_reader_todays_month('temperaturas.csv', '07')
        >>> print(datos['1234X'])
        {'mensual_valor': 35.6, 'mensual_dia': 15, 'mensual_anio': 2022}
    """

    # Leyendo el mes en str
    
    mes_corresp = {
        "01": "ene", "02": "feb", "03": "mar", "04": "abr",
        "05": "may", "06": "jun", "07": "jul", "08": "ago",
        "09": "sep", "10": "oct", "11": "nov", "12": "dec",
    }
    mes_actual_str_letras = mes_corresp[mes_actual_str_number]

    # dic_datos_estaciones: diccionario con todas las temperaturas maximas.
    # Tiene como keys: mensual_valor, mensual_dia, mensual_anio
    dic_datos_estaciones = {}

    with open(ruta_tmax_abs_csv, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)          
        
        col_temp = f"{mes_actual_str_letras}_temp"
        col_dia  = f"{mes_actual_str_letras}_dia"
        col_anio = f"{mes_actual_str_letras}_anio"

        for fila in lector:
            
            # --- Valores maximos del mes
            temp_val = fila[col_temp]
            dia_val = fila[col_dia]
            anio_val = fila[col_anio]

            # Si los valores no son válidos (no son floats)
            if (not es_valor_valido(temp_val) or 
                not es_valor_valido(dia_val) or
                not es_valor_valido(anio_val)):

                logging.info(
                    f"Datos del tmax_reader_todays_month no convertibles (mensuales). Fila idema: {fila['idema']}")
                
                dic_datos_estaciones[fila['idema']] = {
                    'mensual_valor': None,
                    'mensual_dia': None,
                    'mensual_anio': None
                }

            # Si los valores sí son válidos (son floats)
            else:
                dic_datos_estaciones[fila['idema']] = {
                    'mensual_valor': float(temp_val)/10, # se divide entre 10 porque aemet pone "205" en lugar de "20.5"
                    'mensual_dia': int(dia_val),
                    'mensual_anio': int(anio_val)
                }
            
            # --- Valores absolutos
            absoluto_valor_val = fila.get('abs_temp')
            absoluto_dia_val = fila.get('abs_dia')
            absoluto_mes_val = fila.get('abs_mes')
            absoluto_anio_val = fila.get('abs_anio')

            # Si los valores no son válidos (no son floats)
            if (not es_valor_valido(absoluto_valor_val) or 
                not es_valor_valido(absoluto_dia_val) or
                not es_valor_valido(absoluto_mes_val) or
                not es_valor_valido(absoluto_anio_val)):

                logging.info(
                    f"Datos del tmax_reader_todays_month no convertibles (absolutos). Fila idema: {fila['idema']}")

                dic_datos_estaciones[fila['idema']].update({
                    'absoluto_valor': None,
                    'absoluto_dia': None,
                    'absoluto_mes': None,
                    'absoluto_anio': None
                })

            # Si los valores sí son válidos (son floats)
            else:
                if fila['idema'] not in dic_datos_estaciones:
                    dic_datos_estaciones[fila['idema']] = {}
                
                dic_datos_estaciones[fila['idema']].update({
                    'absoluto_valor': float(absoluto_valor_val)/10,
                    'absoluto_dia': int(absoluto_dia_val),
                    'absoluto_mes': int(absoluto_mes_val),
                    'absoluto_anio': int(absoluto_anio_val)
                })

    logging.info("Datos de tem max de este mes leidos del csv.")
    return dic_datos_estaciones