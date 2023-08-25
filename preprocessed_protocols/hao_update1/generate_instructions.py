import openpyxl

XLSX_FILENAME ="opentron template test example.xlsx"

METADATA = {'apiLevel': '2.13',
			'protocolName': 'Protocol test',
			'description': 'This protocol is for testing purpose on robot',
			'author': 'HL'}

INSTRUCTIONS = """
\tCSV_DATA = pd.read_csv(StringIO(data))
\tCSV_DATA = CSV_DATA.replace('None', 0)
\tprint(CSV_DATA)
\tfor STOCK in CSV_DATA.columns:
\t\tif STOCK == "Well_number": continue
\t\tfor index, row in CSV_DATA.iterrows():
\t\t\tvolume = row[STOCK]
\t\t\tdestination_well = row['Well_number']
\t\t\tif pd.notnull(volume) and volume != 0: 
\t\t\t\tsource_well = reservoir.wells_by_name()[STOCK]
\t\t\t\tdestination_well = plate.wells_by_name()[destination_well]
\t\t\t\tp300.transfer(float(volume), source_well, destination_well, new_tip='always', touch_tip=True)
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
        f"\ttiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)\n"
        f"\treservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2)\n"
        f"\tplate = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)\n"
        f"\tp300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])\n"
        f"{INSTRUCTIONS}"
    )

    with open("opentron_input1.py", "w") as text_file:
        text_file.write(input_file)

gen_inputfile(XLSX_FILENAME)