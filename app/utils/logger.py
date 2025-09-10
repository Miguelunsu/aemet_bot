import datetime
import logging

# EJEMPLOS DE LOGS
#logging.debug("Mensaje de debug")
#logging.info("Mensaje informativo")
#logging.warning("Advertencia")
#logging.error("Error")
#logging.critical("Error crítico")

def configurar_logging():
    nombre_log = "aemetlog-" + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(nombre_log, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info(f"Logger configurado correctamente. Nombre de log: {nombre_log}")
    
    return