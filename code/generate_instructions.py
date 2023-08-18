import openpyxl

XLSX_FILENAME ="./data/opentron template test example.xlsx"

METADATA = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.''',
    'author': 'New API User'
    }

INSTRUCTIONS = """
\tCSV_DATA = pd.read_csv(StringIO(data))
\tfor STOCK in CSV_DATA.columns:
\t\tif STOCK == "Well_number": continue
\t\tp300.pick_up_tip()
\t\tp300.distribute(list(CSV_DATA[STOCK]), STOCK, list(CSV_DATA['Well_number']))
\t\tp300.drop_tip()
"""

def gen_inputfile(XLSX_FILENAME):
    wb = openpyxl.load_workbook(XLSX_FILENAME)
    ws = wb.active

    data = ''
    for row in ws.iter_rows(values_only=True):
        if row == (None, None, None, None): break
        
        items = [str(i) for i in row]

        new_list = (','.join(items))
        data = data + new_list + "\n"

    
    input_file = (
        f"# Upload this data/instructions file to the OpenTrons GUI\n"
        f"import pandas as pd\n"
        f"from io import StringIO\n"
        f"from opentrons import protocol_api\n\n"
        f"data = '''\n"
        f"{data}'''\n\n"
        f"metadata = {METADATA}\n\n"
        f"def run(protocol: protocol_api.ProtocolContext):\n"
        f"\ttiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)\n"
        f"\tplate = protocol.load_labware('3dprt_50ml_2x3', 3)\n"
        f"\twell1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)\n"
        f"\tp300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])\n"
        f"{INSTRUCTIONS}"
    )

    with open("./code/opentron_input.py", "w") as text_file:
        text_file.write(input_file)

gen_inputfile(XLSX_FILENAME)