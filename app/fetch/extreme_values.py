
def get_extreme_values(data, meteo_var):
    # data: diccionario que tiene todas las medidas en tiempo real (una por hora)
    # meteo_var: variable meteo de la que queremos los datos extremos por estacion
    
    # Devuelve: variable est_extreme_12h: Nested diccionary de estaciones con los datos de variable max.
    # Key: idema. Dentro: diccionario con fint, tamax, ubi, lat y lon
    
    est_extreme_12h = dict()
    
    print(f"Funcion get_extreme_values. Getting: {meteo_var}")
    for idx, est_i in enumerate(data, start=1):

        idema = est_i.get("idema", "Nan")
        print(f"Estudiando {meteo_var}: {idx}/{len(data)} - {idema}, {est_i.get('fint')}")

        # Si en el diccionario ya hemos visto esta key de idema
        if idema in est_extreme_12h:
            tmax_dummy = est_i.get(meteo_var, "Nan")

            # si el valor de meteo_var presente en el diccionario es NaN...
            if est_extreme_12h[idema][meteo_var] == "Nan": 
                # sea lo que sea, se sustituye. En el peor caso, un Nan se sustituye por un nan
                est_extreme_12h[idema][meteo_var] = tmax_dummy
            # Si la medida de esta hora es Nan, no se hace nada
            elif tmax_dummy == "Nan":
                pass
            # Ver si la temperatura dummy es mayor: se sustituye la tmax y el tiempo de medida
            elif float(tmax_dummy) > float(est_extreme_12h[idema][meteo_var]):
                est_extreme_12h[idema]["fint"] = est_i.get("fint", "Nan")
                est_extreme_12h[idema][meteo_var] = tmax_dummy
        
        # Si es la primera vez que vemos esta key
        else:
            est_extreme_12h[idema] = {
                "fint": est_i.get("fint", "Nan"),
                meteo_var: est_i.get(meteo_var, "Nan"),
                "ubi": est_i.get("ubi", "Nan"),
                "lat": est_i.get("lat", "Nan"),
                "lon": est_i.get("lon", "Nan")
            }
    return est_extreme_12h