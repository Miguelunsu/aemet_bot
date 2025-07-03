import time
import sys
from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url

#from fetch.aemet_client import get_real_time_data
#from db.models import save_to_db
#from utils.parser import parse_obs

#raw_data = get_real_time_data()
#observaciones = parse_obs(raw_data)
#save_to_db(observaciones)

def main():
    print("Iniciando main.", flush=True)

    endpoint = 'https://opendata.aemet.es/opendata/api/observacion/convencional/todas'

    data_url = get_data_url_from_aemet(endpoint)
    data = download_data_from_url(data_url) # Lista de diccionarios de estaciones

    # Mostrar los 3 primeros registros
    for obs in data[:3]:
        print(f"{obs['ubi']} Ta max: {obs['tamax']}. ")

if __name__ == "__main__":
    main()