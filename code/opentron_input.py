import pandas as pd
from io import StringIO
from opentrons import protocol_api

data = '''
Well,A1,A2,A3
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
	plate = protocol.load_labware('3dprt_50ml_2x3', 3)
	well1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

	CSV_DATA = pd.read_csv(StringIO(data))
	for STOCK in CSV_DATA.columns:
		if STOCK == "Well": continue
		p300.pick_up_tip()
		p300.distribute(CSV_DATA[STOCK], STOCK, CSV_DATA['Well'])
		p300.drop_tip()
