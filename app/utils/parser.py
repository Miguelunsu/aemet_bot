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
        - Si es la cadena None, se devuelve un resultado con todos los campos a None.

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
      todos los valores correspondientes se rellenan con None.
    - Los índices se acceden de 0 a 11 (enero–diciembre), por lo que el índice 12
      de las listas no se utiliza.
    - Muestra un mensaje en consola indicando la estación procesada.
    """
    if data == None or data == "Nan": 
        logging.info(f"parser_temp_max: Variable data es Nan. Devolviendo lista de Nans.")     
        idema = None
        temMax_lista = None
        diaMax_lista = None
        anioMax_lista = None
        abs_mes = None
        
    else:
        idema = data.get("indicativo", None)
        temMax_lista = data.get("temMax", None)
        diaMax_lista = data.get("diaMax", None)
        anioMax_lista = data.get("anioMax", None)
        abs_mes = data.get("mesMax", None)

    if isinstance(temMax_lista, list) and len(temMax_lista) == 13 and temMax_lista:
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
        ene_temp = None
        feb_temp = None
        mar_temp = None
        abr_temp = None
        may_temp = None
        jun_temp = None
        jul_temp = None
        ago_temp = None
        sep_temp = None
        oct_temp = None
        nov_temp = None
        dic_temp = None

        abs_temp = None

    if isinstance(diaMax_lista, list) and len(diaMax_lista) == 13 and diaMax_lista:
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
        ene_dia = None
        feb_dia = None
        mar_dia = None
        abr_dia = None
        may_dia = None
        jun_dia = None
        jul_dia = None
        ago_dia = None
        sep_dia = None
        oct_dia = None
        nov_dia = None
        dic_dia = None

        abs_dia = None

    if isinstance(anioMax_lista, list) and len(anioMax_lista) == 13 and anioMax_lista:
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
        ene_anio = None
        feb_anio = None
        mar_anio = None
        abr_anio = None
        may_anio = None
        jun_anio = None
        jul_anio = None
        ago_anio = None
        sep_anio = None
        oct_anio = None
        nov_anio = None
        dic_anio = None

        abs_anio = None

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