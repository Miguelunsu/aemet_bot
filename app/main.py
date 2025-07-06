import time
import os
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from utils.csv_writer import csv_writer_tmax
from utils.parser import parser_temp_max
import csv

def main():
    print(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        print("Iniciando main.", flush=True)

        endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'
        print("Llamando get_data_url_from_aemet...", flush=True)

        data_url = get_data_url_from_aemet(endpoint)
        print(f"data_url: {data_url}", flush=True)

        print("Llamando download_data_from_url...", flush=True)
        data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
        print(f"Datos descargados, cantidad: {len(data)}", flush=True)
        print(f"Tipo de data: {type(data)}")

        print(f"Bucle para enseñar todos los datos:")
        for i in data:
            idema = i.get("fint", "Nan")
            fint = i.get("fint", "Nan")
            tamax = i.get("ubi", "Nan")
            ubi = i.get("tamax", "Nan")
            print(f"Estación {idema}, {fint}, {tamax}, {ubi}")

        ruta_csv_estaciones = os.path.join(BASE_DIR, "estaciones.csv")
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
        
        # Calculo temperaturas extremas
        if True:
            i_counter = 0
            # Bucle temperaturas extremas
            for i_estacion in datos_estaciones:
                i_counter = i_counter + 1
                i_idema = i_estacion.get("idema")

                print(f"Estudiando Tmax en station: {idema}. Station {i_counter}/{len(datos_estaciones)}")
                print("Time sleep: 10")
                time.sleep(10)

                # Endpoint para valores extremos de temperatura
                endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{i_idema}'
                
                print(f"Llamando get_data_url_from_aemet (tempext). Estacion: {i_idema}", flush=True)
                data_url = get_data_url_from_aemet(endpoint)

                print(f"Estacion: {i_idema} -> data_url tempext: {data_url}", flush=True)
                data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo

                dicc_estacion_tmax = parser_temp_max(data)

                temMax = dicc_estacion_tmax.get("temMax")
                diaMax = dicc_estacion_tmax.get("diaMax")
                mesMax = dicc_estacion_tmax.get("mesMax")
                anioMax = dicc_estacion_tmax.get("anioMax")

                file_name = os.path.join(BASE_DIR, "tmax_estaciones.csv")
                if i_counter == 1:
                    # CSV writer con header
                    csv_writer_tmax(file_name, idema, temMax, diaMax, mesMax, anioMax, True)
                else:
                    # CSV writer sin header
                    csv_writer_tmax(file_name, idema, temMax, diaMax, mesMax, anioMax, False)

    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()