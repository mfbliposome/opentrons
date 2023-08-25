import os
from protocols.utils.file_conversion import data_converter, input_file_generator

# Get relative path for 'main.py'
dirname = os.path.dirname(__file__)

# Excel Workbook Data Path
XLSX_FILENAME = os.path.join(dirname, 'data/example_data/opentron template test example.xlsx')
SHEET1, SHEET2 = "Sheet1", "Sheet2"

# Data String obtained from Excel Workbook
DATA = data_converter(XLSX_FILENAME, SHEET1, SHEET2)

# Path to file to be converted for opentron
READ_FILE = os.path.join(dirname, 'protocols/preprocessed/Basic_Transfer.py')

# Destination file path for new opentron input file
WRITE_FILE = os.path.join(dirname, "protocols/postprocessed/Basic_Transfer.py")

# Convert READ_FILE to WRITE_FILE, creating a new input file for opentron in the
# destination folder (opentron_input_files)
input_file_generator(DATA, READ_FILE=READ_FILE, WRITE_FILE=WRITE_FILE)