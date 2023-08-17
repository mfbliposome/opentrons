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

metadata = {'apiLevel': '2.13', 'protocolName': 'Serial Dilution Tutorial', 'description': 'This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.', 'author': 'New API User'}

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
	plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
	# plate = protocol.load_labware('3dprt_50ml_2x3', 3)
	well1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

	CSV_DATA = pd.read_csv(StringIO(data))
	# CSV_DATA = CSV_DATA.fillna(0)
	# for STOCK in CSV_DATA.columns:
	# 	if STOCK == "Well_Number": continue
	# 	p300.pick_up_tip()
	# 	p300.distribute(float(CSV_DATA[STOCK]), STOCK, CSV_DATA['Well_Number'])
	# 	p300.drop_tip()
	# CSV_DATA = CSV_DATA.replace('None', None)
	# CSV_DATA = CSV_DATA.fillna(0)
	CSV_DATA = CSV_DATA.replace('None', 0)
	print(CSV_DATA)
	for STOCK in CSV_DATA.columns:
		if STOCK == "Well_Number":
			continue

		p300.pick_up_tip()
		for index, row in CSV_DATA.iterrows():
			volume = row[STOCK]  # Extract the volume for the current well
			destination_well = row['Well_Number']  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				source_well = well1.wells_by_name()[STOCK]
				destination_well = plate.wells_by_name()[destination_well]

				p300.transfer(float(volume), source_well, destination_well, new_tip='never', touch_tip=True)
		p300.drop_tip()


# for source_well in CSV_DATA.columns:
	# 	if source_well == "Well_Number":
	# 		continue
	#
	# 	source = well1.wells_by_name()[source_well]
	# 	destinations = [plate.wells_by_name()[dest] for dest in CSV_DATA['Well_Number']]
	# 	volumes = CSV_DATA[source_well]
	#
	# 	# Filter out None or NaN volumes
	# 	valid_volumes = [volume for volume in volumes if pd.notnull(volume)]
	#
	# 	if valid_volumes:
	# 		p300.pick_up_tip()
	# 		p300.distribute(valid_volumes, source, destinations, disposal_volume=10)
	# 		p300.drop_tip()

	# for STOCK in CSV_DATA.columns:
	# 	if STOCK == "Well_Number":
	# 		continue
	# 	p300.pick_up_tip()
	# 	for index, row in CSV_DATA.iterrows():
	# 		volume = row[STOCK]  # Extract the volume from the current row and column
	# 		destination_well = row['Well_Number']  # Extract the well to transfer to
	# 		if pd.notnull(volume):  # Check if the volume is not None or NaN
	# 			p300.transfer(volume, plate.wells_by_name()[destination_well], touch_tip=True)
	# 	p300.drop_tip()




