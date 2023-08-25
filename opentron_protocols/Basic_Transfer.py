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
	'author': 'ewroginek & hliu56'
	}

DATA = '''
UNNAMED: 0,A1,A2,A3
A1,10.0,0.0,0.0
A2,10.0,0.0,0.0
A3,10.0,0.0,0.0
A4,10.0,0.0,0.0
A5,0.0,10.0,0.0
A6,0.0,10.0,0.0
A7,0.0,10.0,0.0
A8,0.0,10.0,0.0
A9,0.0,0.0,10.0
A10,0.0,0.0,10.0
A11,0.0,0.0,10.0
A12,0.0,0.0,10.0
B1,5.0,5.0,5.0
B2,10.0,10.0,0.0
B3,10.0,0.0,10.0
B4,6.0,5.0,3.0
B5,0.0,10.0,10.0
B6,20.0,6.0,8.0
B7,8.0,4.0,20.0
B8,3.0,5.0,8.0
B9,6.0,1.0,9.0
B10,9.0,8.0,12.0
B11,12.0,3.0,4.0
B12,4.0,16.0,5.0
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
			destination_well = EXCEL_DATA.iloc[:, 0]  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				source_well = reservoir.wells_by_name()[STOCK]
				destination_well = plate.wells_by_name()[destination_well]
				p300.transfer(float(volume), source_well, destination_well, new_tip='always', touch_tip=True)