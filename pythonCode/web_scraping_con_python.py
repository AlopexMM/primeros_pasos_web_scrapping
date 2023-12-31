import requests
from bs4 import BeautifulSoup

url = "http://localhost:5000/data"

page = requests.get(url)

soup = BeautifulSoup(str(page.content), 'html.parser')

table_data = []

for line in soup.find_all('tr'):
    
    header = line.find_all('th')
    data = line.find_all('td')

    if len(header) != 0:
        table_data.append([data.get_text() for data in header])
    if len(data) != 0:
        table_data.append([data.get_text() for data in data])

# Escribirlo en un archivo de texto

with open("export.txt", "w") as txt_file:
    # Formato en un string
    #|| Fecha      | Venta  | Compra ||
    #|| 2023-10-23 | 1100.0 | 1050.0 ||
    #|| 2023-10-25 | 1000.0 | 950.0  ||
    table_data_to_print = ""
    for line in table_data:
        for i in range (3):
            if i == 0:
                if line[i] == "Fecha":
                    table_data_to_print += f"|| {line[i]}      | "
                else:
                    table_data_to_print += f"|| {line[i]} | "
            if i == 1:
                if line[i] == "Venta":
                    table_data_to_print += f"{line[i]}  | "
                else:
                    if len(line[i]) == 5:
                        table_data_to_print += f"{line[i]}  | "
                    else:
                        table_data_to_print += f"{line[i]} | "
            if i == 2:
                if line[i] == "Compra":
                    table_data_to_print += f"{line[2]} ||\n"
                else:
                    if len(line[i]) == 5:
                        table_data_to_print += f"{line[i]}  ||\n"
                    else:
                        table_data_to_print += f"{line[i]} ||\n"
    txt_file.write(table_data_to_print)

# Escribir en un archivo csv

with open("export.csv", "w") as csv_file:
    # Formato en un string
    table_data_to_print = ""
    for line in table_data:
        for i in range(3):
            if i == 2:
                table_data_to_print += f"{line[i]}\n"
            else:
                table_data_to_print += f"{line[i]},"
    csv_file.write(table_data_to_print)

# Escribir en un archivo json
import json

json_data = []

headers_for_json = []

for line in soup.find_all('tr'):
    
    headers = line.find_all('th')
    data = line.find_all('td')

    if len(headers) != 0:
        for header in headers:
            headers_for_json.append(header.get_text())
    if len(data) >= 1:
        obj = {}
        for i in range(3):
            obj[headers_for_json[i]] = data[i].get_text()
        json_data.append(obj)

json_object = json.dumps(json_data, indent=4)

with open("export.json", "w") as json_file:
    json_file.write(json_object)

from openpyxl import Workbook
import openpyxl


# Escribimos en un excel

wb = Workbook()

ws = wb.active

for line_data in table_data:
    # Sabiendo los datos que se encuentran en la tabla podemos guardar los datos con el formato correcto
    if line_data[0] == "Fecha":
        ws.append(line_data)
    else:
        ws.append([ line_data[0], float(line_data[1]), float(line_data[2]) ])


wb.save("export.xlsx")