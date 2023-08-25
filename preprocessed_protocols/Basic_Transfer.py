# Upload this data/instructions file via the OpenTrons GUI\n"
import os
import pandas as pd
from io import StringIO
from opentrons import protocol_api

metadata = {
	'apiLevel': '2.13',
	'protocolName': os.path.basename(__file__),
	'description': '''
	This simple protocol tests the functionality of the distribute function:
	https://docs.opentrons.com/v2/new_protocol_api.html#opentrons.protocol_api.InstrumentContext.distribute 
	''',
	'author': 'ER & HL'
	}

DATA = """""" # This String will be populated in 'opentron_input_files' after running 'main.py' (do not change!)

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
	reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
	
	EXCEL_DATA = pd.read_csv(StringIO(DATA))
	for STOCK in EXCEL_DATA.columns[1:]:
		for index, row in EXCEL_DATA.iterrows():
			volume = row[STOCK]  # Extract the volume for the current well
			destination_well = EXCEL_DATA.iloc[:, 0]  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				source_well = reservoir.wells_by_name()[STOCK]
				destination_well = plate.wells_by_name()[destination_well]
				p300.transfer(float(volume), source_well, destination_well, new_tip='always', touch_tip=True)