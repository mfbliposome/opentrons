from protocols.utils.file_conversion import setup_postprocessed_file_for
import os

# Data Information
DATA_FILE = "0. SAMPLE_DATA.xlsx"
SHEET1, SHEET2 = "Sheet1", "Sheet2"

# Protocol File
PROTOCOL_FILE = "Basic_Transfer.py"

# Combine Excel Workbook Data with Protocol File
try:
    dirname = os.path.dirname(__file__)
    setup_postprocessed_file_for(dirname, PROTOCOL_FILE, DATA_FILE)

    print(f"Done! Upload './protocols/postprocessed/{PROTOCOL_FILE}' input file to OpenTron GUI")
except:
    print("Data conversion failed :(")
    print("Check filepaths and data organization")