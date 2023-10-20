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
	'author': 'ER & HL'
	}

DATA = '''
DESTINATION_WELL,A1,A2,A3
A1,30,15,100
A2,26,50,15
A3,10,10,25
'''

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
	reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
	
	EXCEL_DATA = pd.read_csv(StringIO(DATA))
	for STOCK in EXCEL_DATA.columns[1:]:
		for index, row in EXCEL_DATA.iterrows():
			volume = row[STOCK]  # Extract the volume for the current well
			destination_wells = list(EXCEL_DATA.iloc[:, 0])  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				p300.pick_up_tip()
				source_well = reservoir.wells_by_name()[STOCK]
				for WELL in destination_wells:
					destination_well = plate.wells_by_name()[WELL]
					p300.transfer(float(volume), source_well, destination_well.bottom(5), new_tip='never', touch_tip=True)
				p300.drop_tip()