
import csv

def csv_writer_tmax (file_name, idema, temMax, diaMax, mesMax, anioMax, header_bool):
    row = [idema, temMax, diaMax, mesMax, anioMax]
    if header_bool == True:
        file = open(file_name,"r+",newline="")
        file.truncate(0) # Clears file

        header = ['idema', 'temMax', 'diaMax', 'mesMax', 'anioMax']

        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write a row to the csv file
            writer.writerow(row)
    else:
        with open(file_name, 'a', encoding='UTF8', newline='') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write a row to the csv file
            writer.writerow(row)
    return