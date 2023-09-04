import pandas as pd
import os

def select_file_from(data_files:list):
    """
    Accepts a list of file paths as a parameter, prompts the user to select a file from
    a list by pressing a number, and returns a file name corresponding to the selected number
    
    Returns: String of file name
    """
    print("Files in the directory:")
    for i, file_name in enumerate(data_files, start=1):
        print(f"{i}. {file_name}")

    # Prompt the user to select a file
    while True:
        try:
            choice = int(input("Enter the number of the file you want to select: "))
            if 1 <= choice <= len(data_files):
                selected_file = data_files[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Return the selected file
    return selected_file

def get_file_from(DIRNAME:str, FOLDER:str, EXAMPLE:str=''):
    """
    Retrieve a file name using a command-line-interface (CLI) for a user
    """
    SELECT_FILE = ''
    while SELECT_FILE != 'y' and SELECT_FILE != 'n':
        SELECT_FILE = input(f"Select data from './{FOLDER}'? [y,n]")

    if SELECT_FILE == 'y':
        files = os.listdir(f'{DIRNAME}/{FOLDER}')
        FILENAME = select_file_from(files)
    else:
        FILENAME = input(f"Enter the name of the file {EXAMPLE}: ")
    
    return FILENAME

def data_converter(XLSX_FILENAME:str, SHEET1:str, SHEET2:str, REAGENT_NAMES:int = 0, REAGENT_LOCATIONS:int = 2):
    """ 
    This function takes an excel workbook and uses the data from the sheet names
    to transform opentron instructions into a data string that can be read by the
    opentron GUI
    
    Returns: String containing comma separated instructions for moving a stock
    volume to the reservior of interest
    """

    # Read in instruction data from Sheet 1 and replace empty cell values with a '0'
    instructions = pd.read_excel(open(XLSX_FILENAME, 'rb'), sheet_name=SHEET1).fillna(0)
    instructions.columns = instructions.columns.str.upper()

    # Read in reagent data from Sheet 2
    reagent_data = pd.read_excel(open(XLSX_FILENAME, 'rb'), sheet_name=SHEET2)
    reagent_data.columns = reagent_data.columns.str.upper()
    REAGENT, LOCATION = reagent_data.columns[REAGENT_NAMES], reagent_data.columns[REAGENT_LOCATIONS]
    reagent_data[REAGENT] = reagent_data[REAGENT].str.upper()
    reagent_data[LOCATION] = reagent_data[LOCATION].str.upper()

    # Create a reagent-location dictionary
    reagent_dict = dict(zip(reagent_data[REAGENT], reagent_data[LOCATION]))
    instructions = instructions.rename(columns=reagent_dict)

    # Build the data string object
    data = ','.join(map(str, instructions.columns)) + '\n'
    for index, row in instructions.iterrows():
        row_string = ','.join(map(str, row))
        data = data + row_string + "\n"
    
    return data

def input_file_generator(DATA:str, READ_FILE:str, WRITE_FILE:str, DATA_COMMENT:str = "DATA = \"\"\"\"\"\""):
    """
    This function takes a DATA String produced by the data_converter() and the file name for the
    READ_FILE protocol of interest and creates a new input file WRITE_FILE, which can be read by
    the opentron. The READ_FILE needs to have a DATA_COMMENT so that the DATA can be inserted.
    """

    if not READ_FILE.endswith(".py"): 
        print("Read File needs to be a .py file")
    elif not WRITE_FILE.endswith(".py"): 
        print("Input file name must be a .py file")
    else:
        with open(WRITE_FILE, 'w') as input_file:
            with open(READ_FILE, 'r') as reader:
                for line in reader:
                    if DATA_COMMENT in line:
                        input_file.write(
                            f"DATA = '''\n"
                            f"{DATA}'''\n"
                        )
                    else:
                        input_file.write(line)

def setup_postprocessed_file_for(dirname:str, PROTOCOL_FILE:str, DATA_FILE:str, SHEET1:str="Sheet1", SHEET2:str="Sheet2"):
    # Excel Workbook Data Path
    XLSX_FILENAME = os.path.join(dirname, f'data/{DATA_FILE}')

    # Data String obtained from Excel Workbook
    DATA = data_converter(XLSX_FILENAME, SHEET1, SHEET2)

    # Path to file to be converted for opentron
    READ_FILE = os.path.join(dirname, f'protocols/preprocessed/{PROTOCOL_FILE}')

    # Destination file path for new opentron input file
    WRITE_FILE = os.path.join(dirname, f"protocols/postprocessed/{PROTOCOL_FILE}")

    # Convert READ_FILE to WRITE_FILE, creating a new input file for opentron in the destination folder (opentron_input_files)
    input_file_generator(DATA, READ_FILE=READ_FILE, WRITE_FILE=WRITE_FILE)