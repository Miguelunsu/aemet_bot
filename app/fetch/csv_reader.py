import csv

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
