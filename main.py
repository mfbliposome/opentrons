import os
from protocols.utils.file_conversion import get_file_from, run_simulator, create_postprocessed_protocol

# Get current working directory
DIRNAME = os.path.dirname(os.path.abspath(__file__))

# Input Data File and Protocol File from the user
DATA_FILE = get_file_from(DIRNAME, 'data', '(e.g., 0. SAMPLE_DATA.xlsx)')
SHEET1 = input("Sheet1 name: ")
SHEET2 = input("Sheet2 name: ")

PROTOCOL_FILE = get_file_from(DIRNAME, 'protocols/preprocessed', '(e.g., Basic_Transfer.py)')

# Combine Excel Workbook Data with Protocol File
create_postprocessed_protocol(DIRNAME, PROTOCOL_FILE, DATA_FILE, SHEET1, SHEET2)

# Test the new protocol file by running the simulator
run_simulator(PROTOCOL_FILE)