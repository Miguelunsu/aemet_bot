import csv
import os

def guardar_valores_en_csv(datos, nombre_csv="prep_acumulado_12h.csv"):
    """
    Lee un diccionario donde cada clave es 'idema' y dentro hay un campo 'valor',
    y guarda esos pares (idema, valor) en un archivo CSV con header.
    
    Ejemplo de 'datos':
    {
        "1234A": {"nombre": "Estación A", "valor": 12.3},
        "5678B": {"nombre": "Estación B", "valor": 5.7},
    }
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(BASE_DIR, nombre_csv)

    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["idema", "value"])  # encabezado

        for idema, info in datos.items():
            value = info.get("value")
            writer.writerow([idema, value])

    print(f"Archivo '{nombre_csv}' creado correctamente.")


def leer_csv_a_diccionario(nombre_csv="prep_acumulado_12h.csv"):
    """
    Lee un CSV con columnas 'idema' y 'value' y devuelve un diccionario:
    {
        idema1: valor1,
        idema2: valor2,
        ...
    }
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(BASE_DIR, nombre_csv)

    datos = {}

    with open(ruta_csv, mode="r", newline="", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            idema = fila["idema"]
            value = float(fila["value"]) if fila["value"] else None
            datos[idema] = value

    return datos

import os

def borrar_csv(nombre_csv="prep_acumulado_12h.csv"):
    """
    Elimina el archivo CSV indicado si existe.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(BASE_DIR, nombre_csv)
    
    # Sobrescribir el archivo con solo el header
    with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["idema", "value"])

    print(f"Contenido de '{ruta_csv}' borrado correctamente (archivo preservado).")
