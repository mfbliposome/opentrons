# Upload this data/instructions file via the OpenTrons GUI\n"
import pandas as pd
from io import StringIO
from opentrons import protocol_api

metadata = {
	'apiLevel': '2.13',
	'protocolName': 'Basic_Transfer', # protocolName should be same name as current file
	'description': '''
	This simple protocol tests the functionality of the distribute function:
	https://docs.opentrons.com/v2/new_protocol_api.html#opentrons.protocol_api.InstrumentContext.distribute 
	''',
	'author': 'ER'
	}

INSTRUCTIONS = """""" # This String will be populated in 'opentron_input_files' after running 'main.py' (do not change!)

def run(protocol: protocol_api.ProtocolContext):
	# Load labware for the experiment
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
	reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
	
	# Load instructions from excel workbook
	EXCEL_DATA = pd.read_csv(StringIO(INSTRUCTIONS))
	SOLUTIONS = EXCEL_DATA.columns[1:]
	DESTINATIONS = list(EXCEL_DATA[EXCEL_DATA.columns[0]])

	# Distribute the stock solutions to their destination wells
	for STOCK_LOCATION in SOLUTIONS:
		STOCK_VOLUMES = list(EXCEL_DATA[STOCK_LOCATION])
		DESTINATION_WELLS = [plate[WELL].bottom(5) for WELL in DESTINATIONS]
		p300.distribute(STOCK_VOLUMES, reservoir[STOCK_LOCATION], DESTINATION_WELLS)