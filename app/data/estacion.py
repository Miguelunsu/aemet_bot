import csv
import os
from datetime import datetime

class Estacion:
    def __init__(self, idema, ubi, lon, lat):
        self.idema = idema
        self.ubi = ubi
        self.lon = float(lon)
        self.lat = float(lat)
    def __repr__(self):
        return f"<Estacion {self.idema} - {self.ubi}>"
        
    
def read_estaciones_from_csv(BASE_DIR):
    # Lee como clases de estaciones todas las estaciones del csv de estaciones

    # Obtencion del path de estaciones.csv
    ruta_csv_estaciones = os.path.join(BASE_DIR, "estaciones.csv")
    
    # Inicializacion y bucle para pillar las estaciones
    estaciones = []
    with open(ruta_csv_estaciones, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            est = Estacion(
                idema = fila['idema'],
                ubi = fila['ubi'],
                lat =  float(fila['lat']),
                lon =  float(fila['lon'])
            )
            estaciones.append(est)
    return estaciones

def encontrar_ubi_con_idema(todas_estaciones, idema):
    # encuentra el string ubi para la estacion con este idema
    # todas_estaciones: lista con clase estaciones
    # idema: idema a encontrar la coincidencia en las estaciones
    for est in todas_estaciones:
        if est.idema == idema:
            return est.ubi
        
def capitalizar_ubi(ubi):
    # Pone presentable la ubi para tweet
    # si hay dos espacios, los sustituye por espacio y coma
    ubi = ubi.replace("  ", ", ")
    # capitaliza todo (todo con mayuscula al principio)
    ubi = ubi.title()
    # convertimos artículos y de a lowercase otra vez
    ubi = ubi.replace(" De ", " de ")
    ubi = ubi.replace(" El ", " el ")
    ubi = ubi.replace(" La ", " la ")
    ubi = ubi.replace(" Los ", " los ")
    ubi = ubi.replace(" Las ", " Las ")
    return ubi

def parser_fint(fint):
    # Parsea el fint. El fint tiene el aspecto "2025-10-19T13:00:00+0000"
    # dt tiene formato fecha con localizacion (datetime.datetime(2025, 10, 19, 13, 0, tzinfo=datetime.timezone.utc)) 
    dt = datetime.strptime(fint, "%Y-%m-%dT%H:%M:%S%z")

    # dt_naive carece de esto (datetime.datetime(2025, 10, 19, 13, 0))
    dt_naive = dt.replace(tzinfo=None)

    return dt_naive