# Upload this data/instructions file to the OpenTrons GUI
import pandas as pd
from io import StringIO
from opentrons import protocol_api

data = '''
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

metadata = {'apiLevel': '2.13', 'protocolName': 'Serial Dilution Tutorial', 'description': 'This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.', 'author': 'New API User'}

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])
	CSV_DATA = pd.read_csv(StringIO(data))
	for STOCK in CSV_DATA.columns[1:]:
		p300.pick_up_tip()
		p300.distribute(list(CSV_DATA[STOCK]), STOCK, list(CSV_DATA['Well_number']))
		p300.drop_tip()
