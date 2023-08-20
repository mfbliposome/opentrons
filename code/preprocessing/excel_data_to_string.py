import pandas as pd

def data_converter(XLSX_FILENAME:str, SHEET1:str, SHEET2:str):
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
    REAGENT, LOCATION = reagent_data.columns[0], reagent_data.columns[2]
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