# Upload this data/instructions file to the OpenTrons GUI
import pandas as pd
from io import StringIO
from opentrons import protocol_api

data = '''
None,A1
A1,50
A2,None
A3,50
A4,None
A5,50
A6,None
A7,50
A8,None
A9,50
A10,None
A11,50
A12,None
B1,None
B2,None
B3,None
B4,None
B5,None
B6,None
B7,None
B8,None
B9,None
B10,None
B11,None
B12,None
C1,50
C2,None
C3,50
C4,None
C5,50
C6,None
C7,50
C8,None
C9,50
C10,None
C11,50
C12,None
D1,None
D2,None
D3,None
D4,None
D5,None
D6,None
D7,None
D8,None
D9,None
D10,None
D11,None
D12,None
E1,50
E2,None
E3,50
E4,None
E5,50
E6,None
E7,50
E8,None
E9,50
E10,None
E11,50
E12,None
F1,None
F2,None
F3,None
F4,None
F5,None
F6,None
F7,None
F8,None
F9,None
F10,None
F11,None
F12,None
G1,50
G2,None
G3,50
G4,None
G5,50
G6,None
G7,50
G8,None
G9,50
G10,None
G11,50
G12,None
H1,None
H2,None
H3,None
H4,None
H5,None
H6,None
H7,None
H8,None
H9,None
H10,None
H11,None
H12,None
'''

metadata = {'apiLevel': '2.13', 'protocolName': 'Serial Dilution Tutorial', 'description': 'This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.', 'author': 'New API User'}

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

	CSV_DATA = pd.read_csv(StringIO(data))
	for STOCK in CSV_DATA.columns:
		if STOCK == "Well_number": continue
		p300.pick_up_tip()
		p300.distribute(list(CSV_DATA[STOCK]), STOCK, list(CSV_DATA['Well_number']))
		p300.drop_tip()
