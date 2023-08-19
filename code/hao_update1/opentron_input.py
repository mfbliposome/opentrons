# Upload this data/instructions file to the OpenTrons GUIimport pandas as pd
from io import StringIO
from opentrons import protocol_api
import pandas as pd

data = '''
Well_Number,A1,A2,A3
A1,10,None,None
A2,10,None,None
A3,10,None,None
A4,10,None,None
A5,None,10,None
A6,None,10,None
A7,None,10,None
A8,None,10,None
A9,None,None,10
A10,None,None,10
A11,None,None,10
A12,None,None,10
B1,5,5,5
B2,10,10,None
B3,10,None,10
B4,6,5,3
B5,None,10,10
B6,20,6,8
B7,8,4,20
B8,3,5,8
B9,6,1,9
B10,9,8,12
B11,12,3,4
B12,4,16,5
'''

metadata = {'apiLevel': '2.13',
			'protocolName': 'Protocol test',
			'description': 'This protocol is for testing purpose on robot',
			'author': 'HL'}

def run(protocol: protocol_api.ProtocolContext):
	# extracting these information from excel file?
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	# need check if the experiment protocol is compatible to the plate (in the future)
	# e.g. if experiment have 12 columns to transfer solutions, the plate has to be
	# 96-well plate, not 24-well plate
	well1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

	CSV_DATA = pd.read_csv(StringIO(data))
	CSV_DATA = CSV_DATA.replace('None', 0)
	print(CSV_DATA)
	for STOCK in CSV_DATA.columns:
		if STOCK == "Well_Number":
			continue

		# p300.pick_up_tip()
		for index, row in CSV_DATA.iterrows():
			volume = row[STOCK]  # Extract the volume for the current well
			destination_well = row['Well_Number']  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				source_well = well1.wells_by_name()[STOCK]
				destination_well = plate.wells_by_name()[destination_well]

				p300.transfer(float(volume), source_well, destination_well, new_tip='always', touch_tip=True)
		# p300.drop_tip()




