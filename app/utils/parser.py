from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url

def parser_temp_max(idema_target):
    # Endpoint para valores extremos de temperatura
    endpoint = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/valoresextremos/parametro/T/estacion/{idema_target}'
    
    print(f"Llamando get_data_url_from_aemet (temp. extremas). Estacion: {idema_target}", flush=True)

    data_url = get_data_url_from_aemet(endpoint)

    print(f"Temp. Extr. Estacion: {idema_target} -> data_url: {data_url}", flush=True)

    data = download_data_from_url(data_url) # Lista de diccionarios de estaciones meteo
    pass
    if data == "Nan":
        idema = "Nan"
        temMax_lista = "Nan"
        diaMax_lista = "Nan"
        anioMax_lista = "Nan"
        mesMax = "Nan"
    else:
        idema = data.get("indicativo", "Nan")
        temMax_lista = data.get("temMax", "Nan")
        diaMax_lista = data.get("diaMax", "Nan")
        anioMax_lista = data.get("anioMax", "Nan")
        mesMax = data.get("mesMax", "Nan")

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
    return {"idema": idema,
            "temMax": temMax,
            "diaMax": diaMax,
            "mesMax": mesMax,
            "anioMax": anioMax
        }
