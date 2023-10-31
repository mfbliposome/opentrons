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
	DECK_SLOTS = INSTRUCT[INSTRUCT.columns[0]] # The first column has deck slot that indicate where the destination plates are located in the OT-2  
	slots = DECK_SLOTS.unique() # Get the slots numbers being used

	# Load labware for the experiment
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 11)
	reservoir = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 10)
	plate1 = protocol.load_labware('nest_96_wellplate_200ul_flat', 1)
	plate2 = protocol.load_labware('nest_96_wellplate_200ul_flat', 2)
	
    # Load pipette and convert to labware object
	PIPETTE_TYPE = pd.read_csv(StringIO(PIPETTE))
	PIPETTE_LOCATION = PIPETTE_TYPE[PIPETTE_TYPE.columns[0]][0]
	PIPETTE_API_NAME = PIPETTE_TYPE[PIPETTE_TYPE.columns[1]][0]
	p = protocol.load_instrument(PIPETTE_API_NAME, PIPETTE_LOCATION, tip_racks=[tiprack])

	plate = [plate1, plate2]
	for i in range(len(slots)):
		# Filter instruction table for plate number of interest
		INST = INSTRUCT[INSTRUCT[INSTRUCT.columns[0]] == slots[i]]
		DESTINATIONS = list(INST[INST.columns[1]])
		SOLUTIONS = INST.columns[2:]

		# Distribute stock solution to the corresponding plate well numbers
		for STOCK_LOCATION in SOLUTIONS:
			STOCK_VOLUMES = list(INST[STOCK_LOCATION])
			DW = [plate[i][WELL].bottom(5) for WELL in DESTINATIONS]
			p.distribute(STOCK_VOLUMES, reservoir[STOCK_LOCATION], DW)