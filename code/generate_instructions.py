import pandas as pd

XLSX_FILENAME ="./data/opentron template test example.xlsx"
SHEET1 = "Sheet1"
SHEET2 = "Sheet2"

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

METADATA = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.''',
    'author': 'New API User'
    }

INSTRUCTIONS = (
    f"\tCSV_DATA = pd.read_csv(StringIO(data))\n"
    f"\tfor STOCK in CSV_DATA.columns[1:]:\n"
    f"\t\tp300.pick_up_tip()\n"
    f"\t\tp300.distribute(list(CSV_DATA[STOCK]), STOCK, list(CSV_DATA['Well_number']))\n"
    f"\t\tp300.drop_tip()\n"
)

def protocol_generator(data, METADATA, INSTRUCTIONS):
    return (
        f"# Upload this data/instructions file to the OpenTrons GUI\n"
        f"import pandas as pd\n"
        f"from io import StringIO\n"
        f"from opentrons import protocol_api\n\n"
        f"data = '''\n"
        f"{data}'''\n\n"
        f"metadata = {METADATA}\n\n"
        f"def run(protocol: protocol_api.ProtocolContext):\n"
        f"\ttiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)\n"
        f"\tp300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])\n"
        f"{INSTRUCTIONS}"
    )

data = data_converter(XLSX_FILENAME, SHEET1, SHEET2)
input_file = protocol_generator(data, METADATA, INSTRUCTIONS)
with open("./code/opentron_input.py", "w") as text_file:
    text_file.write(input_file)