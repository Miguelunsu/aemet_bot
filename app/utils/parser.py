from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
import logging

def parser_temp_max_todos_meses(data):
    """
    Procesa los datos de temperaturas máximas de una estación meteorológica.

    Parámetros
    ----------
    data : dict o str
        - Si es un diccionario: debe contener las claves:
            * "indicativo" : str -> identificador de la estación.
            * "temMax"     : list -> lista con las temperaturas máximas mensuales (índices 1–12).
            * "diaMax"     : list -> lista con los días en los que se alcanzaron esas temperaturas.
            * "anioMax"    : list -> lista con los años en los que se alcanzaron esas temperaturas.
        - Si es la cadena "Nan", se devuelve un resultado con todos los campos a "Nan".

    Retorna
    -------
    dict
        Diccionario con la siguiente estructura:
        {
            "idema": str,
            "ene_temp": str, "ene_dia": str, "ene_anio": str,
            "feb_temp": ..., "feb_dia": ..., "feb_anio": ...,
            ...
            "dic_temp": ..., "dic_dia": ..., "dic_anio": ...
        }

    Notas
    -----
    - Si las listas "temMax", "diaMax" o "anioMax" no existen o no son válidas,
      todos los valores correspondientes se rellenan con "Nan".
    - Los índices se acceden de 0 a 11 (enero–diciembre), por lo que el índice 12
      de las listas no se utiliza.
    - Muestra un mensaje en consola indicando la estación procesada.
    """
    if data == "Nan": 
        logging.info(f"parser_temp_max: Variable data es Nan. Devolviendo lista de Nans.")     
        idema = "Nan"
        temMax_lista = "Nan"
        diaMax_lista = "Nan"
        anioMax_lista = "Nan"
        abs_mes = "Nan"
        
    else:
        idema = data.get("indicativo", "Nan")
        temMax_lista = data.get("temMax", "Nan")
        diaMax_lista = data.get("diaMax", "Nan")
        anioMax_lista = data.get("anioMax", "Nan")
        abs_mes = data.get("mesMax", "Nan")

    if isinstance(temMax_lista, list) and temMax_lista:
        ene_temp = temMax_lista[0]
        feb_temp = temMax_lista[1]
        mar_temp = temMax_lista[2]
        abr_temp = temMax_lista[3]
        may_temp = temMax_lista[4]
        jun_temp = temMax_lista[5]
        jul_temp = temMax_lista[6]
        ago_temp = temMax_lista[7]
        sep_temp = temMax_lista[8]
        oct_temp = temMax_lista[9]
        nov_temp = temMax_lista[10]
        dic_temp = temMax_lista[11]

        abs_temp = temMax_lista[12]
    else:
        ene_temp = "Nan"
        feb_temp = "Nan"
        mar_temp = "Nan"
        abr_temp = "Nan"
        may_temp = "Nan"
        jun_temp = "Nan"
        jul_temp = "Nan"
        ago_temp = "Nan"
        sep_temp = "Nan"
        oct_temp = "Nan"
        nov_temp = "Nan"
        dic_temp = "Nan"

        abs_temp = "Nan"

    if isinstance(diaMax_lista, list) and diaMax_lista:
        ene_dia = diaMax_lista[0]
        feb_dia = diaMax_lista[1]
        mar_dia = diaMax_lista[2]
        abr_dia = diaMax_lista[3]
        may_dia = diaMax_lista[4]
        jun_dia = diaMax_lista[5]
        jul_dia = diaMax_lista[6]
        ago_dia = diaMax_lista[7]
        sep_dia = diaMax_lista[8]
        oct_dia = diaMax_lista[9]
        nov_dia = diaMax_lista[10]
        dic_dia = diaMax_lista[11]

        abs_dia = diaMax_lista[12]
    else:
        ene_dia = "Nan"
        feb_dia = "Nan"
        mar_dia = "Nan"
        abr_dia = "Nan"
        may_dia = "Nan"
        jun_dia = "Nan"
        jul_dia = "Nan"
        ago_dia = "Nan"
        sep_dia = "Nan"
        oct_dia = "Nan"
        nov_dia = "Nan"
        dic_dia = "Nan"

        abs_dia = "Nan"

    if isinstance(anioMax_lista, list) and anioMax_lista:
        ene_anio = anioMax_lista[0]
        feb_anio = anioMax_lista[1]
        mar_anio = anioMax_lista[2]
        abr_anio = anioMax_lista[3]
        may_anio = anioMax_lista[4]
        jun_anio = anioMax_lista[5]
        jul_anio = anioMax_lista[6]
        ago_anio = anioMax_lista[7]
        sep_anio = anioMax_lista[8]
        oct_anio = anioMax_lista[9]
        nov_anio = anioMax_lista[10]
        dic_anio = anioMax_lista[11]

        abs_anio = anioMax_lista[12]
    else:
        ene_anio = "Nan"
        feb_anio = "Nan"
        mar_anio = "Nan"
        abr_anio = "Nan"
        may_anio = "Nan"
        jun_anio = "Nan"
        jul_anio = "Nan"
        ago_anio = "Nan"
        sep_anio = "Nan"
        oct_anio = "Nan"
        nov_anio = "Nan"
        dic_anio = "Nan"

        abs_anio = "Nan"

    logging.info(f"Estación {idema}: obtención de todas las temperaturas completada.")
    return {"idema": idema,
            "ene_temp": ene_temp,
            "ene_dia": ene_dia,
            "ene_anio": ene_anio,
            "ene_temp": ene_temp,
            
            "feb_temp": feb_temp,
            "feb_dia": feb_dia,
            "feb_anio": feb_anio,

            "mar_temp": mar_temp,
            "mar_dia": mar_dia,
            "mar_anio": mar_anio,
            
            "abr_temp": abr_temp,
            "abr_dia": abr_dia,
            "abr_anio": abr_anio,
            
            "may_temp": may_temp,
            "may_dia": may_dia,
            "may_anio": may_anio,
            
            "jun_temp": jun_temp,
            "jun_dia": jun_dia,
            "jun_anio": jun_anio,
            
            "jul_temp": jul_temp,
            "jul_dia": jul_dia,
            "jul_anio": jul_anio,
            
            "ago_temp": ago_temp,
            "ago_dia": ago_dia,
            "ago_anio": ago_anio,
            
            "sep_temp": sep_temp,
            "sep_dia": sep_dia,
            "sep_anio": sep_anio,
            
            "oct_temp": oct_temp,
            "oct_dia": oct_dia,
            "oct_anio": oct_anio,
            
            "nov_temp": nov_temp,
            "nov_dia": nov_dia,
            "nov_anio": nov_anio,
            
            "dic_temp": dic_temp,
            "dic_dia": dic_dia,
            "dic_anio": dic_anio,
            
            "abs_temp": abs_temp,
            "abs_dia": abs_dia,
            "abs_mes": abs_mes,
            "abs_anio": abs_anio}