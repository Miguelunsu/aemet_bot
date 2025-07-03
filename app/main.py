import time
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url

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
        while True:
            print("Estoy vivo...")
            time.sleep(10)
    except:
        print(f"Error en main", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()