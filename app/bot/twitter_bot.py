import os
from dotenv import load_dotenv
import tweepy
import logging

from data.estacion import read_estaciones_from_csv, encontrar_ubi_con_idema, capitalizar_ubi, parser_fint

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# -------------------------------
# Credenciales para autenticar el bot
# -------------------------------
# NO usamos bearer_token porque necesitamos publicar tweets
api_key = os.getenv("TWITTER_API_KEY")             # API Key de la app
api_secret = os.getenv("TWITTER_API_SECRET")       # API Secret Key de la app
access_token = os.getenv("TWITTER_ACCESS_TOKEN")   # Access Token del usuario
access_secret = os.getenv("TWITTER_ACCESS_SECRET") # Access Token Secret del usuario

# -------------------------------
# Crear el cliente Tweepy con User Context
# Esto permite publicar tweets, no solo leer datos
# -------------------------------
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_secret
)

# Función para publicar un tweet
def post_tweet(tweet_text: str):
    """
    Publica un tweet con el texto proporcionado.
    Args:
        tweet_text (str): Texto que se quiere publicar en Twitter.
    """
    response = client.create_tweet(text=tweet_text)    # Llama al endpoint POST /2/tweets
    print("Tweet publicado con ID:", response.data["id"])  # Muestra en consola el ID del tweet

def mes_en_string_con_integer(mes_number):
    mes_number = str(mes_number)
    mes_corresp = {
        "1":'enero',
        "2":'febrero',
        "3":'marzo',
        "4":'abril',
        "5":'mayo',
        "6":'junio',
        "7":'julio',
        "8":'agosto',
        "9":'septiembre',
        "10":'octubre',
        "11":'noviembre',
        "12":'diciembre'
    }
    mes_actual_str_letras = mes_corresp[mes_number]
    return mes_actual_str_letras

def create_tweet(record_superado, previous_record_info, idema, variable_record, mensual_o_abs, BASE_DIR):
    """
    Escribe el tweet
    Args:
        record_superado:
        previous_record_info:
        datos_actuales:
        idema:
        variable_record:                temp_max or pluv_max
        mensual_o_abs:                  record del mes o absoluto
        BASE_DIR: para el csv de las estaciones
    """
    if not (variable_record == "temp_max" or variable_record == "pluv_max"):
        raise Exception
    
    # Lee todas las estaciones que tenemos de referencia
    todas_estaciones = read_estaciones_from_csv(BASE_DIR)

    # Busca la ubi con el idema que tiene
    ubi = encontrar_ubi_con_idema(todas_estaciones, idema)
    # Modificamos la ubi para ponerla correcta
    ubi_ok = capitalizar_ubi(ubi)

    # Obtener la fecha y hora del fint en modo datetime
    date_fint = parser_fint(record_superado["fint"])

    # ajustar decimales de records
    record_superado_valor = round(float(record_superado["value"]), 1)
    if record_superado_valor.is_integer():
        record_superado_str = str(int(record_superado_valor))
    else:
        record_superado_str = f"{record_superado_valor:.1f}"
    
    previous_record_valor = round(float(previous_record_info["value"]), 1)
    if previous_record_valor.is_integer():
        previous_record_str = str(int(previous_record_valor))
    else:
        previous_record_str = f"{previous_record_valor:.1f}"

    # Tweet para temperaturas maximas
    if variable_record == "temp_max":

        if mensual_o_abs == "abs":

            tweet =f"❗La estación de {ubi_ok} ha superado el récord histórico de máxima temperatura registrada.\n"\
                f"Se ha registrado una temperatura de {record_superado_str}ºC el "\
                f"{date_fint.strftime("%d")} de {mes_en_string_con_integer(date_fint.strftime("%m"))} a las {date_fint.strftime("%H:%M")}.\n"\
                f"El anterior récord era de {previous_record_str}ºC, registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        elif mensual_o_abs == "mensual":
            tweet =f"La estación de {ubi_ok} ha superado el récord de máxima temperatura registrada en {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"Se ha registrado una temperatura de {record_superado_str}ºC el "\
                f"{date_fint.strftime("%d")} de {mes_en_string_con_integer(date_fint.strftime("%m"))} a las {date_fint.strftime("%H:%M")}.\n"\
                f"El anterior récord era de {previous_record_str}ºC, registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        else:
            raise Exception  
    # Tweet para lluvia maximas
    elif variable_record == "pluv_max":
        if mensual_o_abs == "abs":
            tweet =f"❗La estación de {ubi_ok} ha superado el récord histórico de máxima precipitación acumulada registrada.\n"\
                f"Se ha registrado una precipitación acumulada de {record_superado_str}mm el "\
                f"{date_fint.strftime("%d")} de {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"El anterior récord era de {previous_record_str}mm, registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        elif mensual_o_abs == "mensual":
            tweet =f"La estación de {ubi_ok} ha superado el récord de máxima precipitación acumulada registrada en {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"Se ha registrado una precipitación acumulada de {record_superado_str}mm el "\
                f"{date_fint.strftime("%d")} de {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"El anterior récord era de {previous_record_str}mm, registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        else:
            raise Exception  

    else:
        raise Exception           
    return tweet

def tweet_manager(  records_superados_temp_bool,
                    previous_record_temp_info,
                    max_temp_12h_estaciones,
                    records_superados_pluv_bool,
                    previous_record_pluv_info,
                    sum_pluv_12h_estaciones,
                    sumar_o_guardar_cum,
                    BASE_DIR):
    # Esta función, con toda la info de los records, lanza el tweet que se necesita.
    # la funcion sumar_o_guardar_cum guarda o suma los comulativos de un csv (para lluvias)

    # keys que contienen los idemas que superaron la T max
    idemas_tmax_mes_superada = []
    for key, valores in records_superados_temp_bool.items():
        if valores.get("valor_superado_mes") is True:
            idemas_tmax_mes_superada.append(key)
            if valores.get("valor_superado_abs") is True:
                logging.info(f"{key} Temp: superada la ABSOLUTA. Día de hoy{max_temp_12h_estaciones[key]}. Día histórico{previous_record_temp_info[key]}.")
                tweet_text = create_tweet(max_temp_12h_estaciones[key],
                                previous_record_temp_info[key],
                                key,
                                "temp_max",
                                "abs",
                                BASE_DIR)
                
                post_tweet(tweet_text)
            else:
                logging.info(f"{key} Temp: superada la MENSUAL. Día de hoy{max_temp_12h_estaciones[key]}. Día histórico{previous_record_temp_info[key]}.")
                tweet_text = create_tweet(max_temp_12h_estaciones[key],
                                previous_record_temp_info[key],
                                key,
                                "temp_max",
                                "mensual",
                                BASE_DIR)
                
                post_tweet(tweet_text)

    for key, valores in records_superados_pluv_bool.items():
        if valores.get("valor_superado_mes") is True:
            idemas_tmax_mes_superada.append(key)
            if valores.get("valor_superado_abs") is True:
                logging.info(f"{key} Prec: superada la ABSOLUTA. Día de hoy{max_temp_12h_estaciones[key]}. Día histórico{previous_record_temp_info[key]}.")

                tweet_text = create_tweet(sum_pluv_12h_estaciones[key],
                                previous_record_pluv_info[key],
                                key,
                                "pluv_max",
                                "abs",
                                BASE_DIR)
                
                post_tweet(tweet_text)
            else:
                logging.info(f"{key} Prec: superada la MENSUAL. Día de hoy{max_temp_12h_estaciones[key]}. Día histórico{previous_record_temp_info[key]}.")

                tweet_text = create_tweet(sum_pluv_12h_estaciones[key],
                                previous_record_pluv_info[key],
                                key,
                                "pluv_max",
                                "mensual",
                                BASE_DIR)
                
                post_tweet(tweet_text)
    
    logging.info("Fin tweet_manager")