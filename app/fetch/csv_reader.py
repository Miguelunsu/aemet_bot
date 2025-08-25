import csv
from utils.auxiliar import string_a_float_con_decimal
import pandas as pd

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

def tmax_reader_todays_month(ruta_tmax_abs_csv, mes_actual_str_number):
    """
    Lee las temperaturas máximas absolutas del mes actual desde un archivo CSV.
    
    Args:
        ruta_tmax_abs_csv (str): Ruta del archivo CSV con los datos de temperaturas
        mes_actual_str_number (str): Número del mes en formato '01' a '12'
    
    Returns:
        est_tmax_abs: Diccionario con las temperaturas máximas por estación (idema).
                      Cada entrada contiene temperatura, día y año del récord mensual.
                      Los valores inválidos se retornan como None.
    
    Example:
        >>> datos = tmax_reader_todays_month('temperaturas.csv', '07')
        >>> print(datos['1234X'])
        {'mes_target_temMax': 35.6, 'mes_target_diaMax': 15, 'mes_target_anioMax': 2022}
    """

    # Leyendo el mes en str
    
    mes_corresp = {
        "01": "ene",
        "02": "feb",
        "03": "mar", 
        "04": "abr",
        "05": "may",
        "06": "jun",
        "07": "jul",
        "08": "ago",
        "09": "sep",
        "10": "oct",
        "11": "nov",
        "12": "dec",
    }

    mes_actual_str_letras = mes_corresp[mes_actual_str_number]

    est_tmax_abs = {}
    # est_tmax_abs: diccionario con todas las temperaturas maximas. Tiene como keys: mes_target_temMax, mes_target_diaMax, mes_target_anioMax

    with open(ruta_tmax_abs_csv, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)          
        for fila in lector:
            # Valores de la columna (depende del mes)
            temp_val = fila[mes_actual_str_letras + "_temp"]
            dia_val = fila[mes_actual_str_letras + "_dia"]
            anio_val = fila[mes_actual_str_letras + "_anio"]
            
            # Verificar si alguno es NaN o vacío
            if (temp_val == 'Nan' or temp_val == 'Nan' or temp_val == 'Nan' or 
                temp_val == '' or dia_val == '' or anio_val == ''):
                
                est_tmax_abs[fila['idema']] = {
                    'mes_target_temMax': None,
                    'mes_target_diaMax': None,
                    'mes_target_anioMax': None
                }
            else:
                est_tmax_abs[fila['idema']] = {
                    'mes_target_temMax': float(temp_val)/10, # se divide entre 10 porque aemet pone "205" en lugar de "20.5"
                    'mes_target_diaMax': int(dia_val),
                    'mes_target_anioMax': int(anio_val)
                }
    print("Datos de tem max de este mes leidos del csv.")
    return est_tmax_abs