from preprocessing.excel_data_to_string import data_converter
from preprocessing.protocols import Distribute_Dilution

# Excel Workbook Data
DATA_PATH = "./data"
XLSX_FILENAME = f"{DATA_PATH}/opentron template test example.xlsx"
SHEET1 = "Sheet1"
SHEET2 = "Sheet2"

# Data string obtained from Excel Workbook
DATA = data_converter(XLSX_FILENAME, SHEET1, SHEET2)

# Input File output data
OUTPUT_PATH = "./opentron_input_files"
OUTPUT_FILENAME = f"{OUTPUT_PATH}/serial_dilution_tutorial.py"

# Create Input File and write to destination folder
input_file = Distribute_Dilution(DATA).input_file_generator()
with open(OUTPUT_FILENAME, "w") as text_file:
    text_file.write(input_file)