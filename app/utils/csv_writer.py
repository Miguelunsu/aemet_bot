import csv

def csv_writer_tmax_todos_meses (file_name, i_idema, dicc_estacion_tmax2, header_bool):
    
    # En caso de que el dicc tenga un idema NAN, lo cambiamos por el idema del bucle de main
    if dicc_estacion_tmax2["idema"] == "Nan":
        dicc_estacion_tmax2["idema"] = i_idema
        
    if header_bool == True:
        file = open(file_name,"r+",newline="")
        file.truncate(0) # Clears file

        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.DictWriter(f,fieldnames=dicc_estacion_tmax2.keys())
            # Escribiendo el header
            writer.writeheader()
            # write a row to the csv file
            writer.writerow(dicc_estacion_tmax2)
    else:
        with open(file_name, 'a', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.DictWriter(f,fieldnames=dicc_estacion_tmax2.keys())

            # write a row to the csv file
            writer.writerow(dicc_estacion_tmax2)
    return

