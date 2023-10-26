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

# These Strings will be populated in 'opentron_input_files' after running 'main.py' (do not change!)
INSTRUCTIONS = """"""
LABWARE = """"""
PIPETTE = """"""

def run(protocol: protocol_api.ProtocolContext):
	# Load instructions from excel workbook
	INSTRUCT = pd.read_csv(StringIO(INSTRUCTIONS))
	DECK_SLOTS = list(INSTRUCT[INSTRUCT.columns[0]]) # The first column has deck slot that indicate where the destination plates are located in the OT-2  
	DESTINATIONS = list(INSTRUCT[INSTRUCT.columns[1]])
	SOLUTIONS = INSTRUCT.columns[2:]

	# Load labware for the experiment
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 11)
	reservoir = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', 10)
	plate1 = protocol.load_labware('nest_96_wellplate_200ul_flat', 1)
	plate2 = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)
	
    # Load pipette and convert to labware object
	PIPETTE_TYPE = pd.read_csv(StringIO(PIPETTE))
	PIPETTE_LOCATION = PIPETTE_TYPE[PIPETTE_TYPE.columns[0]][0]
	PIPETTE_API_NAME = PIPETTE_TYPE[PIPETTE_TYPE.columns[1]][0]
	p = protocol.load_instrument(PIPETTE_API_NAME, PIPETTE_LOCATION, tip_racks=[tiprack])

	# Distribute the stock solutions to their destination wells
	for STOCK_LOCATION in SOLUTIONS:
		STOCK_VOLUMES = list(INSTRUCT[STOCK_LOCATION])
		DW1 = [plate1[WELL].bottom(5) for WELL in DESTINATIONS]
		p.distribute(STOCK_VOLUMES, reservoir[STOCK_LOCATION], DW1)
		
    	# Distribute the stock solutions to their destination wells
	for STOCK_LOCATION in SOLUTIONS:
		STOCK_VOLUMES = list(INSTRUCT[STOCK_LOCATION])
		DW2 = [plate2[WELL].bottom(5) for WELL in DESTINATIONS]
		p.distribute(STOCK_VOLUMES, reservoir[STOCK_LOCATION], DW2)