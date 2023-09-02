from protocols.utils.file_conversion import setup_postprocessed_file_for
import os

# Input Data File and Protocol File from the user
DATA_FILE = input("Enter the name of the data file (e.g., 0. SAMPLE_DATA.xlsx): ")
PROTOCOL_FILE = input("Enter the name of the protocol file (e.g., Basic_Transfer.py): ")

SHEET1, SHEET2 = "Sheet1", "Sheet2"

# Combine Excel Workbook Data with Protocol File
try:
    dirname = os.path.dirname(__file__)
    setup_postprocessed_file_for(dirname, PROTOCOL_FILE, DATA_FILE)

    print(f"Done! Upload './protocols/postprocessed/{PROTOCOL_FILE}' input file to OpenTron GUI")
except:
    print("Data conversion failed :(")
    print("Check filepaths and data organization")