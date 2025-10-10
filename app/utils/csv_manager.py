import os
import glob
import shutil
import re
import logging

def actualizar_csv(BASE_DIR, nombre_csv):
    """
    Función que busca y copia el CSV más reciente con nombre que coincide con nombre_csv

    BASE_DIR: directorio base de main
    nombre_csv: nombre del csv (ejemplo: tmax_estaciones)
    """
    if nombre_csv not in ["tmax_estaciones"]:
        raise Exception
    
    # Buscar todos los archivos que coincidan con el patrón
    archivos = glob.glob(os.path.join(BASE_DIR, str(nombre_csv+"_*.csv")))
    
    if not archivos:
        logging.error("No se encontraron archivos CSV con el patrón 'tmax_estaciones_*.csv'")
        return False
    
    # Extraer fechas y encontrar el más reciente
    archivos_con_fechas = []
    for archivo in archivos:
        nombre = os.path.basename(archivo)
        # Buscar el formato _YYYYMMDD.csv
        match = re.search(r'tmax_estaciones_(\d{8})\.csv$', nombre)
        if match:
            fecha = int(match.group(1))
            archivos_con_fechas.append((archivo, fecha, nombre))
    
    if not archivos_con_fechas:
        print("No se encontraron archivos con formato de fecha válido (YYYYMMDD)")
        return False
    
    # Ordenar por fecha (más reciente primero)
    archivos_con_fechas.sort(key=lambda x: x[1], reverse=True)
    archivo_mas_reciente, fecha, nombre_original = archivos_con_fechas[0]
    
    # Ruta de destino
    archivo_destino = os.path.join(BASE_DIR, "tmax_estaciones.csv")
    
    try:
        # Copiar el archivo
        shutil.copy2(archivo_mas_reciente, archivo_destino)
        print(f"Copiado: {nombre_original} → tmax_estaciones.csv")
        print(f"Fecha del archivo: {fecha}")
        return True
        
    except Exception as e:
        print(f"Error al copiar: {e}")
        return False