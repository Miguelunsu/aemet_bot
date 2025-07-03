import time
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
from utils.csv_writer import csv_writer_tmax
import csv
import collections

def main():
    print(f"Python version: {sys.version}")
    
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
        
        # Temperaturas extremas
        idema_target = 5783
        endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{idema_target}'
        print(f"Llamando get_data_url_from_aemet (temp. extremas). Estacion: {idema_target}", flush=True)

        print(f"Temp. Extr. Estacion: {idema_target} -> data_url: {data_url}", flush=True)
        data_url = get_data_url_from_aemet(endpoint)
        print("Llamando download_data_from_url...", flush=True)
        data2 = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
        idema = data2.get("indicativo", "Nan")
        temMax_lista = data2.get("temMax", "Nan")
        diaMax_lista = data2.get("diaMax", "Nan")
        anioMax_lista = data2.get("anioMax", "Nan")
        mesMax = data2.get("mesMax", "Nan")

        if isinstance(temMax_lista, list) and temMax_lista:
            temMax = temMax_lista[-1]
        else:
            temMax = "Nan"

        if isinstance(diaMax_lista, list) and diaMax_lista:
            diaMax = diaMax_lista[-1]
        else:
            diaMax = "Nan"

        if isinstance(anioMax_lista, list) and anioMax_lista:
            anioMax = anioMax_lista[-1]
        else:
            anioMax = "Nan"

        print(f"Estación {idema}. Temp. max. Valor: {temMax}. Fecha: {diaMax}/{mesMax}/{anioMax}")
        
        csv_writer_tmax(idema, temMax, diaMax, mesMax, anioMax, True)
        csv_writer_tmax(idema, temMax, diaMax, mesMax, anioMax, False)

    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()