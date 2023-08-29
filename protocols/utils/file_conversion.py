import pandas as pd

def data_converter(XLSX_FILENAME:str, SHEET1:str, SHEET2:str, REAGENT_NAMES:int = 0, REAGENT_LOCATIONS:int = 2):
    """ 
    This function takes an excel workbook and uses the data from the sheet names
    to transform opentron instructions into a data string that can be read by the
    opentron GUI
    
    returns: String containing comma separated instructions for moving a stock
    volume to the reservior of interest
    """

    # Read in instruction data from Sheet 1 and replace empty cell values with a '0'
    instructions = pd.read_excel(open(XLSX_FILENAME, 'rb'), sheet_name=SHEET1).fillna(0)
    instructions.columns = instructions.columns.str.upper()

    # Read in reagent data from Sheet 2
    reagent_data = pd.read_excel(open(XLSX_FILENAME, 'rb'), sheet_name=SHEET2)
    reagent_data.columns = reagent_data.columns.str.upper()
    REAGENT, LOCATION = reagent_data.columns[REAGENT_NAMES], reagent_data.columns[REAGENT_LOCATIONS]
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