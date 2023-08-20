from preprocessing.excel_data_to_string import data_converter
from preprocessing.protocols import Serial_Dilution_Tutorial

XLSX_FILENAME ="./data/opentron template test example.xlsx"
SHEET1 = "Sheet1"
SHEET2 = "Sheet2"

DATA = data_converter(XLSX_FILENAME, SHEET1, SHEET2)
input_file = Serial_Dilution_Tutorial(DATA).input_file_generator()
with open("./input_files/serial_dilution_tutorial.py", "w") as text_file:
    text_file.write(input_file)