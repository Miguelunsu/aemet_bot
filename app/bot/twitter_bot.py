import os                       # Permite acceder a variables de entorno
from dotenv import load_dotenv  # Carga variables del archivo .env
import tweepy                   # Librería oficial de Twitter/X para Python
import time
from datetime import datetime
from datetime import date
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

# Función disparador para las horas
def scheduler(horas=["00:10","12:10"]):
    
    ejecutado_hoy = dict.fromkeys(horas, True)

    while True:
        ahora = datetime.now()
        hora_actual = f"{ahora.hour:02d}:{ahora.minute:02d}" # formato 00:10

        # Comprobar cada hora objetivo
        for objetivo in ejecutado_hoy:
            if hora_actual == objetivo and not ejecutado_hoy[objetivo]:
                post_tweet(f"Test hora {hora_actual}")
                ejecutado_hoy[objetivo] = True

        # Reiniciar flags a la primera hora marcada en la variable horas
        if hora_actual == horas[0]:
            for key in ejecutado_hoy:
                ejecutado_hoy[key] = False

        time.sleep(30)  # Espera 30 segundos antes de volver a comprobar

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

    # Tweet para temperaturas maximas
    if variable_record == "temp_max":
        if mensual_o_abs == "abs":
            tweet =f"❗La estación de {ubi_ok} ha superado el récord histórico de máxima temperatura registrada.\n"\
                f"Se ha registrado una temperatura de {record_superado["value"]}ºC el "\
                f"{date_fint.strftime("%D")} de {mes_en_string_con_integer(date_fint.strftime("%m"))} a las {date_fint.strftime("%H:%M")}.\n"\
                f"El anterior récord era de {previous_record_info["value"]}ºC registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        elif mensual_o_abs == "mensual":
            tweet =f"La estación de {ubi_ok} ha superado el récord de máxima temperatura registrada en {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"Se ha registrado una temperatura de {record_superado["value"]}ºC el "\
                f"{date_fint.strftime("%D")} de {mes_en_string_con_integer(date_fint.strftime("%m"))} a las {date_fint.strftime("%H:%M")}.\n"\
                f"El anterior récord era de {previous_record_info["value"]}ºC registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        else:
            raise Exception  
    # Tweet para lluvia maximas
    elif variable_record == "pluv_max":
        if mensual_o_abs == "abs":
            tweet =f"❗La estación de {ubi_ok} ha superado el récord histórico de máxima precipitación acumulada registrada.\n"\
                f"Se ha registrado una precipitación acumulada de {record_superado["value"]}mm el "\
                f"{date_fint.strftime("%D")} de {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"El anterior récord era de {previous_record_info["value"]}mm registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        elif mensual_o_abs == "mensual":
            tweet =f"La estación de {ubi_ok} ha superado el récord de máxima precipitación acumulada registrada en {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"Se ha registrado una precipitación acumulada de {record_superado["value"]}mm el "\
                f"{date_fint.strftime("%D")} de {mes_en_string_con_integer(date_fint.strftime("%m"))}.\n"\
                f"El anterior récord era de {previous_record_info["value"]}mm registrado el "\
                f"{previous_record_info["dia"]}/{previous_record_info["mes"]}/{previous_record_info["anio"]}."
        else:
            raise Exception  
        
        


    else:
        raise Exception           
    return tweet