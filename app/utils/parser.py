from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url

def parser_temp_max(data):
    # data: Lista de diccionarios de estaciones meteoç
    # si data es un Nan, devuelve lista de Nans
    if data == "Nan": 
        print("Variable data es Nan. Devolviendo lista de Nans.")
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
