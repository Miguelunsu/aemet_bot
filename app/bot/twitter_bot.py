import os                       # Permite acceder a variables de entorno
from dotenv import load_dotenv  # Carga variables del archivo .env
import tweepy                   # Librería oficial de Twitter/X para Python
import time
from datetime import datetime

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
