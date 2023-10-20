import pandas as pd
import subprocess
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
    files = [i for i in os.listdir(f'{DIRNAME}/{FOLDER}') if i.endswith('.xlsx') or i.endswith('.py')]
    if len(files) == 1:
        return files[0]

    SELECT_FILE = ''
    while SELECT_FILE != 'y' and SELECT_FILE != 'n':
        SELECT_FILE = input(f"Select data from './{FOLDER}'? [y,n]")

    if SELECT_FILE == 'y':
        FILENAME = select_file_from(files)
    else:
        FILENAME = input(f"Enter the name of the file {EXAMPLE}: ")
    
    return FILENAME

def data_converter(XLSX_FILENAME:str, REAGENT_NAMES:int = 0, REAGENT_LOCATIONS:int = 2):
    """ 
    This function takes an excel workbook and uses the data from the sheet names
    to transform opentron instructions into a data string that can be read by the
    opentron GUI
    
    Returns: String containing comma separated instructions for moving a stock
    volume to the reservior of interest
    """

    # Read in instruction data from Sheet 1 and replace empty cell values with a '0'
    print(f"in data_converter() {XLSX_FILENAME}")
    DATA = pd.read_excel(XLSX_FILENAME, None)
    sheet_name = list(DATA.keys())

    # Read in instructions and reagent data from the 1st and 2nd sheets
    instructions = DATA[sheet_name[0]].fillna(0)
    reagent_data = DATA[sheet_name[1]].fillna(0)

    # Obtain column information of interest and standardize strings
    instructions.columns = instructions.columns.str.upper()
    reagent_data.columns = reagent_data.columns.str.upper()
    REAGENT, LOCATION = reagent_data.columns[REAGENT_NAMES], reagent_data.columns[REAGENT_LOCATIONS]
    reagent_data[REAGENT] = reagent_data[REAGENT].str.upper()
    reagent_data[LOCATION] = reagent_data[LOCATION].str.upper()

    # Create a reagent-location dictionary
    reagent_dict = dict(zip(reagent_data[REAGENT], reagent_data[LOCATION]))
    instructions = instructions.rename(columns=reagent_dict)

    # Build the instruction string object
    instruction_string = ','.join(map(str, instructions.columns)) + '\n'
    for index, row in instructions.iterrows():
        row_string = ','.join(map(str, row))
        instruction_string = instruction_string + row_string + "\n"
    
    # Read in Labware and Pipette information from the 3rd and 4th sheet
    labware = DATA[sheet_name[2]].fillna(0)
    pipette = DATA[sheet_name[3]].fillna(0)
    
    # Obtain column information of interest and standardize strings
    labware.columns = labware.columns.str.upper()
    pipette.columns = pipette.columns.str.upper()
    
    # Build the labware string object
    labware_string = ','.join(map(str, labware.columns)) + '\n'
    for index, row in labware.iterrows():
        row_string = ','.join(map(str, row))
        labware_string = labware_string + row_string + "\n"

    # Build the labware string object
    pipette_string = ','.join(map(str, pipette.columns)) + '\n'
    for index, row in pipette.iterrows():
        row_string = ','.join(map(str, row))
        pipette_string = pipette_string + row_string + "\n"

    return instruction_string, labware_string, pipette_string

def input_file_generator(DATA:str, LABWARE:str, PIPETTE:str, READ_FILE:str, WRITE_FILE:str, DATA_COMMENT:str = "INSTRUCTIONS = \"\"\"\"\"\"", LABWARE_COMMENT:str = "LABWARE = \"\"\"\"\"\"", PIPETTE_COMMENT:str = "PIPETTE = \"\"\"\"\"\""):
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
                            f"INSTRUCTIONS = '''\n"
                            f"{DATA}'''\n\n"
                        )
                    elif LABWARE_COMMENT in line:
                        input_file.write(
                            f"LABWARE = '''\n"
                            f"{LABWARE}'''\n\n"
                        )
                    elif PIPETTE_COMMENT in line:
                        input_file.write(
                            f"PIPETTE = '''\n"
                            f"{PIPETTE}'''\n\n"
                        )
                    else:
                        input_file.write(line)

def create_postprocessed_protocol(DIRNAME:str, PROTOCOL_FILE:str, DATA_FILE:str):
    try:
        # Excel Workbook Data Path
        XLSX_FILENAME = os.path.join(DIRNAME, f'data/{DATA_FILE}')

        # Data String obtained from Excel Workbook
        DATA, LABWARE, PIPETTE = data_converter(XLSX_FILENAME)
        
        # Path to file to be converted for opentron
        READ_FILE = os.path.join(DIRNAME, f'protocols/preprocessed/{PROTOCOL_FILE}')
        
        # Destination file path for new opentron input file
        if not os.path.exists(os.path.join(DIRNAME, f"protocols/postprocessed")): os.mkdir(os.path.join(DIRNAME, f"protocols/postprocessed"))
        WRITE_FILE = os.path.join(DIRNAME, f"protocols/postprocessed/{PROTOCOL_FILE}")
        
        # Convert READ_FILE to WRITE_FILE, creating a new input file for opentron in the destination folder (opentron_input_files)
        input_file_generator(DATA, LABWARE, PIPETTE, READ_FILE=READ_FILE, WRITE_FILE=WRITE_FILE)

        # Completed
        print(f"Done! Upload './protocols/postprocessed/{PROTOCOL_FILE}' input file to OpenTron GUI")
    except Exception as error:
        print("Data conversion failed :(")
        print(f"{type(error).__name__}: {error}")

def run_simulator(PROTOCOL_FILE):
    SIMULATOR = ''
    while SIMULATOR != 'y' and SIMULATOR != 'n':
        SIMULATOR = input("Run simulator [y/n]?")

    if SIMULATOR == 'y': 
        try: 
            subprocess.run(f"opentrons_simulate ./protocols/postprocessed/{PROTOCOL_FILE}")
            print("Simulation complete!")
        except Exception as error: 
            print("Failed to run simulator :(")
            print(f"{type(error).__name__}: {error}")