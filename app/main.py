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

        dicc_maximas_temp = dict() # nested diccionary
        print(f"Bucle de todas las temperaturas:")
        for idx, i in enumerate(data, start=1):

            idema = i.get("idema", "Nan")

            # Debugging
            if idema == "0016A":
                pass

            print(f"Estudiando: {idx}/{len(data)} - {idema}, {i.get('fint')}")
            # Si en el diccionario ya hemos visto esta key de idema
            if idema in dicc_maximas_temp:

                tmax_dummy = i.get("tamax", "Nan")
                if dicc_maximas_temp[idema]["tamax"].lower() == "nan": # si la temepratura presente en el diccionario es NaN...
                    dicc_maximas_temp[idema]["tamax"] = tmax_dummy # sea lo que sea, se sustituye. En el peor caso, un Nan se sustituye por un nan
                elif tmax_dummy.lower() == "nan": # Si la medida de esta hora es Nan, no se hace nada
                    pass
                # Ver si la temperatura dummy es mayor: se sustituye la tmax y el tiempo de medida
                elif float(tmax_dummy) > float(dicc_maximas_temp[idema]["tamax"]):
                    dicc_maximas_temp[idema]["fint"] = i.get("fint", "Nan")
                    dicc_maximas_temp[idema]["tamax"] = tmax_dummy
            
            # Si es la primera vez que vemos esta key, se pone directamente los datos de fint, tamax, ubi lat y lon
            else:
                dicc_maximas_temp[idema] = {
                    "fint": i.get("fint", "Nan"),
                    "tamax": i.get("tamax", "Nan"),
                    "ubi": i.get("ubi", "Nan"),
                    "lat": i.get("lat", "Nan"),
                    "lon": i.get("lon", "Nan")
                }

        # Reading a csv from tmax_estaciones_fijadas (maximos de temperaturas de estaciones)
        ruta_csv_tmax = os.path.join(BASE_DIR, "tmax_estaciones_fijadas.csv")
        dicc_tmax = {} # diccionario con todas las temperaturas maximas. Contiene idema, temMax, diaMax, mesMax, anioMax

        def string_a_float_con_decimal(s):
            try:
                s = str(s).strip()  # por si viene como número o con espacios
                if len(s) < 2:
                    return float(s)  # ej: "5" → 5.0
                return float(s[:-1] + '.' + s[-1])
            except (ValueError, TypeError):
                return None  # o lanza una excepción

        with open(ruta_csv_tmax, newline='', encoding='utf-8') as csvfile:
            lector = csv.DictReader(csvfile)
            for fila in lector:
                dicc_tmax[fila['idema']] = {
                    'temMax': fila['temMax'],
                    'diaMax': float(fila['diaMax']),
                    'mesMax': float(fila['mesMax']),
                    'anioMax': float(fila['anioMax'])
                    }
        print("Datos de tem max fetcheados del csv")

        # Crear un nuevo diccionario a partir del viajeo diccionario de estaciones
        # Este es un scenario que estara lleno de true o falses
        dicc_extremos_estaciones = dict.fromkeys(dicc_maximas_temp)
        for key in dicc_maximas_temp.keys():
            dicc_extremos_estaciones[key] = {
                "Tmax_superada": False,
                "Pluvmax_superada": False}

        # Bucle para ver si hay alguna estación en la que se ha superado la tmax
        print("Bucle para ver si la estacion tiene tmax superada")
        for idema in dicc_maximas_temp:
            print(f"evaluando idema para tmax: {idema}")
            tmax_str = dicc_maximas_temp[idema]["tamax"]

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

            dicc_tmax_info = dicc_tmax.get(idema)
            if dicc_tmax_info:
                temMax_abs_str = dicc_tmax_info.get("temMax")

                # Saltar si el valor histórico no es válido
                if not temMax_abs_str or str(temMax_abs_str).lower() == "nan":
                    print(f"⚠️ temMax histórica no válida para {idema}: {temMax_abs_str}. Saltando...")
                    continue

                temMax_abs = string_a_float_con_decimal(temMax_abs_str)
                
                if temMax_abs is not None and tmax > temMax_abs:
                    print(f"✅ T máxima superada en {idema}: actual {tmax} > histórica {temMax_abs}")
                    dicc_extremos_estaciones[idema]["Tmax_superada"] = True
            else:
                print(f"No se encontró una tmax para el idema {idema}")

        
        print("📈 Estaciones que superaron su T máxima:")
        for key, valores in dicc_extremos_estaciones.items():
            if valores.get("Tmax_superada") is True:
                print(f"- {key}")


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