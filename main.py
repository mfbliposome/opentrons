from protocols.utils.file_conversion import get_file_from, setup_postprocessed_file_for
import os

# Get current working directory
DIRNAME = os.path.dirname(os.path.abspath(__file__))

# Input Data File and Protocol File from the user
DATA_FILE = get_file_from(DIRNAME, 'data', '(e.g., 0. SAMPLE_DATA.xlsx)')
PROTOCOL_FILE = get_file_from(DIRNAME, 'protocols/postprocessed', '(e.g., Basic_Transfer.py)')
SHEET1, SHEET2 = "Sheet1", "Sheet2"

# Combine Excel Workbook Data with Protocol File
try:
    setup_postprocessed_file_for(DIRNAME, PROTOCOL_FILE, DATA_FILE)

    print(f"Done! Upload './protocols/postprocessed/{PROTOCOL_FILE}' input file to OpenTron GUI")
except:
    print("Data conversion failed :(")
    print("Check filepaths and data organization")