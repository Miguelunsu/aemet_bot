import logging

def get_station_max_last12h(data, meteo_var):
    # data: diccionario que tiene todas las medidas en tiempo real (una por hora)
    # meteo_var: variable meteo de la que queremos los datos extremos por estacion
    
    # Devuelve: variable est_extreme_12h: Nested diccionary de estaciones con los datos de variable max.
    # Key: idema. Dentro: diccionario con fint (hora), tamax, ubi, lat y lon
    
    est_extreme_12h = dict()
    
    logging.info(f"Funcion get_station_max_last12h. Getting: {meteo_var}")
    for idx, est_i in enumerate(data, start=1):

        idema = est_i.get("idema", "Nan")
        logging.info(f"Estudiando {meteo_var}: {idx}/{len(data)} - {idema}, {est_i.get('fint')}")

        # Si en el diccionario ya hemos visto esta key de idema
        if idema in est_extreme_12h:
            value_dummy = est_i.get(meteo_var, "Nan")

            # si el valor de meteo_var presente en el diccionario es NaN...
            if est_extreme_12h[idema]["value"] == "Nan": 
                # sea lo que sea, se sustituye. En el peor caso, un Nan se sustituye por un nan
                est_extreme_12h[idema]["value"] = value_dummy
            # Si la medida de esta hora es Nan, no se hace nada
            elif value_dummy == "Nan":
                pass
            # Ver si la temperatura dummy es mayor: se sustituye la tmax y el tiempo de medida
            elif float(value_dummy) > float(est_extreme_12h[idema]["value"]):
                est_extreme_12h[idema]["fint"] = est_i.get("fint", "Nan")
                est_extreme_12h[idema]["value"] = value_dummy
        
        # Si es la primera vez que vemos esta key
        else:
            est_extreme_12h[idema] = {
                "fint": est_i.get("fint", "Nan"),
                "value": est_i.get(meteo_var, "Nan"),
                "ubi": est_i.get("ubi", "Nan"),
                "lat": est_i.get("lat", "Nan"),
                "lon": est_i.get("lon", "Nan")
            }
    return est_extreme_12h

def get_station_sum_last12h(data, meteo_var):

    est_extreme_12h = dict()
    
    logging.info(f"Funcion get_station_sum_last12h. Getting: {meteo_var}")
    for idx, est_i in enumerate(data, start=1):

        idema = est_i.get("idema", "Nan")
        logging.info(f"Estudiando {meteo_var}: {idx}/{len(data)} - {idema}, {est_i.get('fint')}")

        # Si en el diccionario ya hemos visto esta key de idema
        if idema in est_extreme_12h:
            value_dummy = est_i.get(meteo_var, "Nan")
            # si el valor de meteo_var presente en el diccionario es NaN...
            if est_extreme_12h[idema]["value"] == "Nan" or None: 
                # vamos a dejar unicamente el valor nuevo. Supongamos que el NaN es cero y seguimos.
                est_extreme_12h[idema]["value"] = value_dummy
            # Si la medida de esta hora es Nan, no se hace nada
            elif value_dummy == "Nan":
                pass
            # si nada de esto ocurre y es un float: sumamos lo que habia a lo de antes
            elif float(value_dummy):
                est_extreme_12h[idema]["fint"] = est_i.get("fint", "Nan") # ponemos la última fint para que quede claro que es el sumatorio de las 12 horas medidas antes de esa fint
                est_extreme_12h[idema]["value"] = est_extreme_12h[idema]["value"] + value_dummy
        
        # Si es la primera vez que vemos esta key
        else:
            est_extreme_12h[idema] = {
                "fint": est_i.get("fint", "Nan"), # el fint no tiene sentido porque la ultima hora no dice nada mas que la ultima hora de la suma
                "value": est_i.get(meteo_var, "Nan"),
                "ubi": est_i.get("ubi", "Nan"),
                "lat": est_i.get("lat", "Nan"),
                "lon": est_i.get("lon", "Nan")
            }
    return est_extreme_12h