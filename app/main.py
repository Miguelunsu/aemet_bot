import os
import sys
import logging

from utils.csv_manager import actualizar_csv
from utils.logger import configurar_logging
from utils.auxiliar import scheduler
from fetch.extreme_csv_writer_from_aemet import lectura_absolutas_aemet

# horas a las que se activa el bot (lapso de 12 horas para que el cumulative prec funcione)
horas_scheduler = ["23:59","23:45"]

def lecutura_extremos_actualizar_csvs(BASE_DIR):
    # Leyendo datos de todas las estaciones (temp y pluv) y actualiza los csvs
    
    lectura_absolutas_aemet(BASE_DIR)

    # Copiar el ultimo csv generado por lectura_absolutas_aemet
    actualizar_csv(BASE_DIR, "tmax_estaciones")
    actualizar_csv(BASE_DIR, "pluvmax_estaciones")

def main():
    # Configurar logs
    configurar_logging()
    
    logging.info(f"Python version: {sys.version}")
    
    # Ruta al archivo CSV relativa al archivo actual. Usado para csv's.
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Actualizar los csvs
    if False:
        lecutura_extremos_actualizar_csvs()

    # Scheduler
    # Encontrar los records y llamar al tweetmanager que hace el tweet
    scheduler(BASE_DIR,
              horas=horas_scheduler)
    
if __name__ == "__main__":
    main()