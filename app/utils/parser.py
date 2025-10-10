from fetch.aemet_client import get_data_url_from_aemet, download_data_from_url
import logging

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']

def procesar_lista(lista, longitud_esperada=13, devolver_abs=False):
    """
    Valida y procesa una lista de datos mensuales.
    Devuelve los 12 primeros valores o el valor absoluto (índice 12).
    Retorna None o lista de None si no es válida.
    """
    if isinstance(lista, list) and len(lista) == longitud_esperada:
        return lista[12] if devolver_abs else lista[:12]
    return None if devolver_abs else [None] * 12

def resultado_vacio():
    """
    Genera un diccionario con todas las claves esperadas inicializadas en None.
    Incluye valores mensuales y absolutos.
    """
    return {
        "idema": None,
        **{f"{mes}_temp": None for mes in MESES},  # dict comprehension
        **{f"{mes}_dia": None for mes in MESES},
        **{f"{mes}_anio": None for mes in MESES},
        "abs_temp": None,
        "abs_dia": None,
        "abs_mes": None,
        "abs_anio": None,
    }

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

    # Manejo del caso None/"Nan"
    if data is None or data == "Nan": 
        logging.info("parser_temp_max: Variable data es Nan. Devolviendo lista de Nones.")
        return resultado_vacio()
    
    # Extracción con valores por defecto
    idema = data.get("indicativo")
    abs_mes = data.get("mesMax")
    
    # Procesar las 3 listas de una vez (evita código repetido)
    temps = procesar_lista(data.get("temMax"))
    dias = procesar_lista(data.get("diaMax")) 
    años = procesar_lista(data.get("anioMax"))
    
    # Temperatura absoluta (índice 12) con validación
    abs_temp = procesar_lista(data.get("temMax"), devolver_abs=True)
    abs_dia = procesar_lista(data.get("diaMax"), devolver_abs=True)
    abs_anio = procesar_lista(data.get("anioMax"), devolver_abs=True)
    
    # Construcción dinámica del diccionario (evita 36 líneas repetitivas)
    resultado = {"idema": idema}
    
    # Bucle para agregar todos los meses automáticamente
    for i, mes in enumerate(MESES):
        resultado.update({
            f"{mes}_temp": temps[i],
            f"{mes}_dia": dias[i],
            f"{mes}_anio": años[i]
        })
    
    # Agregar valores absolutos
    resultado.update({
        "abs_temp": abs_temp,
        "abs_dia": abs_dia, 
        "abs_mes": abs_mes,
        "abs_anio": abs_anio
    })
    
    logging.info(f"Estación {idema}: obtención de todas las temperaturas completada.")
    return resultado

def parser_pluv_max_todos_meses(data):
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

    # Manejo del caso None/"Nan"
    if data is None or data == "Nan": 
        logging.info("parser_temp_max: Variable data es Nan. Devolviendo lista de Nones.")
        return resultado_vacio()
    
    # Extracción con valores por defecto
    idema = data.get("indicativo")
    abs_mes = data.get("mesMax")
    
    # Procesar las 3 listas de una vez (evita código repetido)
    temps = procesar_lista(data.get("temMax"))
    dias = procesar_lista(data.get("diaMax")) 
    años = procesar_lista(data.get("anioMax"))
    
    # Temperatura absoluta (índice 12) con validación
    abs_temp = procesar_lista(data.get("temMax"), devolver_abs=True)
    abs_dia = procesar_lista(data.get("diaMax"), devolver_abs=True)
    abs_anio = procesar_lista(data.get("anioMax"), devolver_abs=True)
    
    # Construcción dinámica del diccionario (evita 36 líneas repetitivas)
    resultado = {"idema": idema}
    
    # Bucle para agregar todos los meses automáticamente
    for i, mes in enumerate(MESES):
        resultado.update({
            f"{mes}_temp": temps[i],
            f"{mes}_dia": dias[i],
            f"{mes}_anio": años[i]
        })
    
    # Agregar valores absolutos
    resultado.update({
        "abs_temp": abs_temp,
        "abs_dia": abs_dia, 
        "abs_mes": abs_mes,
        "abs_anio": abs_anio
    })
    
    logging.info(f"Estación {idema}: obtención de todas las temperaturas completada.")
    return resultado

def parser_pluv_max_todos_meses(data):
    """
    Procesa los datos de temperaturas máximas de una estación meteorológica.

    Parámetros
    ----------
    data : dict o str
        - Si es un diccionario: debe contener las claves:
            * "indicativo" : str -> identificador de la estación.
            * "precMaxDia"     : list -> lista con las temperaturas máximas mensuales (índices 1–12).
            * "diaMaxDia"     : list -> lista con los días en los que se alcanzaron esas temperaturas.
            * "anioMaxDia"    : list -> lista con los años en los que se alcanzaron esas temperaturas.
        - Si es la cadena None, se devuelve un resultado con todos los campos a None.

    Retorna
    -------
    dict
        Diccionario con la siguiente estructura:
        {
            "idema": str,
            "ene_pluv": str, "ene_dia": str, "ene_anio": str,
            "feb_pluv": ..., "feb_dia": ..., "feb_anio": ...,
            ...
            "dic_pluv": ..., "dic_dia": ..., "dic_anio": ...
        }

    Notas
    -----
    - Si las listas "precMaxDia", "diaMaxDia" o "anioMaxDia" no existen o no son válidas,
      todos los valores correspondientes se rellenan con None.
    - Los índices se acceden de 0 a 11 (enero–diciembre), por lo que el índice 12
      de las listas no se utiliza.
    - Muestra un mensaje en consola indicando la estación procesada.
    """

    # Manejo del caso None/"Nan"
    if data is None or data == "Nan": 
        logging.info("parser_pluv_max: Variable data es Nan. Devolviendo lista de Nones.")
        return resultado_vacio()
    
    # Extracción con valores por defecto
    idema = data.get("indicativo")
    abs_mes = data.get("mesMaxDia") # dia porque estoy estudiando los maximos DIARIOS
    
    # Procesar las 3 listas de una vez (evita código repetido)
    temps = procesar_lista(data.get("precMaxDia"))
    dias = procesar_lista(data.get("diaMaxDia")) 
    años = procesar_lista(data.get("anioMaxDia"))
    
    # Temperatura absoluta (índice 12) con validación
    abs_pluv = procesar_lista(data.get("precMaxDia"), devolver_abs=True)
    abs_dia = procesar_lista(data.get("diaMaxDia"), devolver_abs=True)
    abs_anio = procesar_lista(data.get("anioMaxDia"), devolver_abs=True)
    
    # Construcción dinámica del diccionario (evita 36 líneas repetitivas)
    resultado = {"idema": idema}
    
    # Bucle para agregar todos los meses automáticamente
    for i, mes in enumerate(MESES):
        resultado.update({
            f"{mes}_pluv": temps[i],
            f"{mes}_dia": dias[i],
            f"{mes}_anio": años[i]
        })
    
    # Agregar valores absolutos
    resultado.update({
        "abs_pluv": abs_pluv,
        "abs_dia": abs_dia, 
        "abs_mes": abs_mes,
        "abs_anio": abs_anio
    })
    
    logging.info(f"Estación {idema}: obtención de todas las temperaturas completada.")
    return resultado