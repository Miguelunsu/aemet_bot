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

        # Calculo temperaturas extremas
        if False:
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

        # Obtención de medidas en tiempo real
        endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'
        print("Llamando get_data_url_from_aemet...", flush=True)

        data_url = get_data_url_from_aemet(endpoint)
        print(f"data_url: {data_url}", flush=True)

        print("Llamando download_data_from_url...", flush=True)
        data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
        print(f"Datos descargados, cantidad: {len(data)}", flush=True)
        print(f"Tipo de data: {type(data)}")

        dicc_maximas_temp = dict() # nested diccionary
        print(f"Bucle para enseñar todos los datos:")
        for idx, i in enumerate(data, start=1):
            idema = i.get("idema", "Nan")
            print(f"{idx}/{len(data)} - {idema}, {i.get('fint')}")
            if idema == "B614E":
                pass

            # Si en el diccionario ya hemos visto esta key de idema
            if idema in dicc_maximas_temp:
                tmax_dummy = i.get("tamax", "Nan")
                if dicc_maximas_temp[idema]["tamax"] == "Nan": # la temepratura anterior es NaN
                    dicc_maximas_temp[idema]["tamax"] == i.get("tamax", "Nan") # Sea lo que sea, se sustituye. En el peor caso, sera un Nan
                elif tmax_dummy == "Nan": # Si la medida de esta hora es Nan, no se hace nada
                    pass
                # Ver si la temperatura dummy es mayor: se sustituye la tmax y el tiempo de medida
                elif float(tmax_dummy) > float(dicc_maximas_temp[idema]["tamax"]):
                    dicc_maximas_temp[idema]["fint"] = i.get("fint", "Nan")
                    dicc_maximas_temp[idema]["tamax"] = i.get("tamax", "Nan")
            
            # Si es la primera vez que vemos esta key
            else:
                dicc_maximas_temp[idema] = {
                    "fint": i.get("fint", "Nan"),
                    "tamax": i.get("tamax", "Nan"),
                    "ubi": i.get("ubi", "Nan"),
                    "lat": i.get("lat", "Nan"),
                    "lon": i.get("lon", "Nan")
                }
            # print(f"Estación {idema}, {fint}, {tamax}, {ubi}")

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
        

    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()