# Upload this data/instructions file via the OpenTrons GUI\n"
import pandas as pd
from io import StringIO
from opentrons import protocol_api

metadata = {
	'apiLevel': '2.13',
	'protocolName': 'CE_Basic_Transfer', # protocolName should be same name as current file
	'description': '''
	This simple protocol tests the functionality of the distribute function:
	https://docs.opentrons.com/v2/new_protocol_api.html#opentrons.protocol_api.InstrumentContext.distribute 
	''',
	'author': 'CE'
	}

DATA = '''
DESTINATION_WELL,A1,A2,A3,A4,A5,A6,B1,B2,B3,B4,B5,B6,C1,C2,C3,C4,C5,C6,D1
A1,18.5,0.0,0.0,10.0,0.0,0.0,18.0,0.0,0.0,17.0,0.0,0.0,12.5,0.0,0.0,0.0,19.5,10.5,0.0
A2,0.0,0.0,10.5,12.0,0.0,0.0,10.5,0.0,0.0,6.5,0.0,0.0,16.5,0.0,0.0,16.5,0.0,0.0,11.5
A3,10.0,0.0,0.0,10.0,0.0,0.0,0.0,12.0,0.0,8.5,0.0,0.0,15.5,0.0,0.0,15.5,0.0,12.5,0.0
A4,5.5,0.0,0.0,9.0,0.0,0.0,17.5,0.0,0.0,19.5,0.0,0.0,0.0,6.0,0.0,5.0,0.0,0.0,10.0
A5,9.0,0.0,0.0,0.0,0.0,16.5,0.0,0.0,9.0,17.0,0.0,0.0,8.5,0.0,0.0,17.0,0.0,0.0,0.5
A6,18.5,0.0,0.0,13.0,0.0,0.0,0.0,12.5,0.0,0.0,17.0,0.0,6.5,0.0,0.0,10.5,0.0,9.5,0.0
A7,14.0,0.0,0.0,6.5,0.0,0.0,17.5,0.0,0.0,16.5,0.0,0.0,8.5,0.0,0.0,10.5,0.0,15.5,0.0
A8,19.0,0.0,0.0,19.5,0.0,0.0,9.0,0.0,0.0,13.0,0.0,0.0,15.0,0.0,0.0,7.0,0.0,8.5,0.0
A9,18.5,0.0,0.0,6.0,0.0,0.0,19.5,0.0,0.0,14.0,0.0,0.0,11.0,0.0,0.0,9.0,0.0,4.5,0.0
A10,16.0,0.0,0.0,0.0,18.5,0.0,5.5,0.0,0.0,7.5,0.0,0.0,5.5,0.0,0.0,7.0,0.0,13.0,0.0
A11,0.0,9.0,0.0,18.0,0.0,0.0,9.0,0.0,0.0,0.0,12.5,0.0,19.5,0.0,0.0,5.5,0.0,18.5,0.0
A12,0.0,18.0,0.0,0.0,20.0,0.0,14.5,0.0,0.0,9.0,0.0,0.0,12.5,0.0,0.0,11.5,0.0,0.0,17.5
B1,0.0,16.0,0.0,19.0,0.0,0.0,0.0,18.5,0.0,15.5,0.0,0.0,13.5,0.0,0.0,0.0,6.5,0.0,12.0
B2,4.5,0.0,0.0,0.0,0.0,5.5,12.5,0.0,0.0,15.0,0.0,0.0,18.0,0.0,0.0,17.0,0.0,0.0,3.0
B3,9.5,0.0,0.0,0.0,0.0,3.0,0.0,16.5,0.0,12.0,0.0,0.0,12.5,0.0,0.0,8.0,0.0,10.5,0.0
B4,15.0,0.0,0.0,4.5,0.0,0.0,0.0,0.0,13.0,4.5,0.0,0.0,9.5,0.0,0.0,18.0,0.0,16.0,0.0
B5,5.5,0.0,0.0,6.5,0.0,0.0,11.5,0.0,0.0,6.5,0.0,0.0,11.0,0.0,0.0,0.0,2.5,14.0,0.0
B6,7.5,0.0,0.0,13.5,0.0,0.0,0.0,0.0,12.0,13.0,0.0,0.0,8.5,0.0,0.0,14.0,0.0,13.0,0.0
B7,0.0,10.0,0.0,6.0,0.0,0.0,7.0,0.0,0.0,17.5,0.0,0.0,0.0,15.0,0.0,4.0,0.0,10.0,0.0
B8,5.5,0.0,0.0,0.0,12.0,0.0,0.0,8.5,0.0,6.0,0.0,0.0,0.0,19.5,0.0,6.5,0.0,11.5,0.0
B9,12.5,0.0,0.0,0.0,9.5,0.0,19.0,0.0,0.0,4.5,0.0,0.0,4.0,0.0,0.0,16.5,0.0,0.0,16.0
B10,7.5,0.0,0.0,6.0,0.0,0.0,6.5,0.0,0.0,16.0,0.0,0.0,0.0,15.5,0.0,17.5,0.0,0.0,14.0
B11,12.0,0.0,0.0,0.0,4.5,0.0,15.5,0.0,0.0,12.0,0.0,0.0,7.5,0.0,0.0,0.0,10.0,10.0,0.0
B12,10.5,0.0,0.0,7.5,0.0,0.0,0.0,12.5,0.0,0.0,10.5,0.0,12.0,0.0,0.0,0.0,19.0,0.0,7.5
C1,17.0,0.0,0.0,18.0,0.0,0.0,17.0,0.0,0.0,5.0,0.0,0.0,8.5,0.0,0.0,13.5,0.0,6.5,0.0
C2,15.5,0.0,0.0,18.0,0.0,0.0,18.0,0.0,0.0,11.0,0.0,0.0,18.5,0.0,0.0,0.0,11.5,16.5,0.0
C3,15.0,0.0,0.0,15.0,0.0,0.0,16.5,0.0,0.0,14.0,0.0,0.0,0.0,12.5,0.0,16.0,0.0,7.5,0.0
C4,9.5,0.0,0.0,10.0,0.0,0.0,14.0,0.0,0.0,17.5,0.0,0.0,12.0,0.0,0.0,0.0,6.5,16.0,0.0
C5,16.5,0.0,0.0,11.0,0.0,0.0,12.0,0.0,0.0,8.0,0.0,0.0,15.0,0.0,0.0,0.0,13.5,0.0,15.5
C6,10.0,0.0,0.0,10.5,0.0,0.0,7.0,0.0,0.0,15.0,0.0,0.0,12.0,0.0,0.0,0.0,8.5,14.0,0.0
C7,17.5,0.0,0.0,14.0,0.0,0.0,18.0,0.0,0.0,10.5,0.0,0.0,17.5,0.0,0.0,18.5,0.0,6.5,0.0
C8,18.0,0.0,0.0,13.5,0.0,0.0,13.5,0.0,0.0,10.5,0.0,0.0,0.0,0.0,0.5,13.5,0.0,18.0,0.0
C9,10.5,0.0,0.0,19.5,0.0,0.0,0.0,10.5,0.0,20.0,0.0,0.0,7.0,0.0,0.0,10.5,0.0,13.0,0.0
C10,17.5,0.0,0.0,0.0,0.0,11.0,10.5,0.0,0.0,0.0,7.0,0.0,18.0,0.0,0.0,16.0,0.0,12.5,0.0
C11,7.0,0.0,0.0,10.5,0.0,0.0,4.5,0.0,0.0,13.0,0.0,0.0,0.0,0.0,9.5,16.0,0.0,5.0,0.0
C12,16.5,0.0,0.0,6.0,0.0,0.0,0.0,16.0,0.0,0.0,6.0,0.0,15.5,0.0,0.0,13.5,0.0,8.5,0.0
D1,16.0,0.0,0.0,9.0,0.0,0.0,5.5,0.0,0.0,14.5,0.0,0.0,12.5,0.0,0.0,13.0,0.0,7.0,0.0
D2,4.0,0.0,0.0,16.0,0.0,0.0,0.0,9.0,0.0,16.5,0.0,0.0,8.0,0.0,0.0,0.0,14.0,0.0,14.5
D3,8.5,0.0,0.0,17.5,0.0,0.0,5.0,0.0,0.0,6.5,0.0,0.0,18.5,0.0,0.0,8.0,0.0,19.0,0.0
D4,0.0,0.0,18.0,9.5,0.0,0.0,0.0,0.0,0.5,0.0,0.0,13.0,12.5,0.0,0.0,11.0,0.0,11.0,0.0
D5,7.0,0.0,0.0,0.0,5.5,0.0,13.5,0.0,0.0,10.0,0.0,0.0,18.0,0.0,0.0,8.0,0.0,9.5,0.0
D6,12.5,0.0,0.0,17.0,0.0,0.0,16.5,0.0,0.0,5.5,0.0,0.0,13.0,0.0,0.0,0.0,16.5,19.0,0.0
D7,0.0,20.0,0.0,8.0,0.0,0.0,0.0,10.0,0.0,20.0,0.0,0.0,8.5,0.0,0.0,12.0,0.0,5.0,0.0
D8,14.5,0.0,0.0,11.5,0.0,0.0,16.0,0.0,0.0,12.0,0.0,0.0,20.0,0.0,0.0,14.0,0.0,5.5,0.0
D9,12.0,0.0,0.0,18.0,0.0,0.0,5.0,0.0,0.0,5.0,0.0,0.0,0.0,8.0,0.0,5.0,0.0,9.5,0.0
D10,14.5,0.0,0.0,13.5,0.0,0.0,5.5,0.0,0.0,17.0,0.0,0.0,0.0,7.0,0.0,14.5,0.0,0.0,0.0
D11,4.5,0.0,0.0,9.5,0.0,0.0,0.0,19.5,0.0,0.0,0.0,18.5,10.0,0.0,0.0,11.5,0.0,10.0,0.0
D12,6.0,0.0,0.0,5.5,0.0,0.0,5.0,0.0,0.0,10.0,0.0,0.0,18.0,0.0,0.0,10.5,0.0,11.0,0.0
E1,10.0,0.0,0.0,12.5,0.0,0.0,0.0,5.5,0.0,0.0,13.5,0.0,0.0,4.0,0.0,14.0,0.0,19.5,0.0
E2,0.0,17.0,0.0,17.5,0.0,0.0,11.5,0.0,0.0,12.5,0.0,0.0,0.0,12.0,0.0,14.0,0.0,0.0,6.5
E3,0.0,6.0,0.0,17.0,0.0,0.0,0.0,0.0,1.0,8.5,0.0,0.0,10.0,0.0,0.0,6.0,0.0,16.5,0.0
E4,0.0,19.0,0.0,13.5,0.0,0.0,8.5,0.0,0.0,19.0,0.0,0.0,0.0,0.0,1.5,4.5,0.0,11.0,0.0
E5,8.0,0.0,0.0,19.5,0.0,0.0,0.0,16.5,0.0,0.0,0.0,0.5,9.5,0.0,0.0,6.5,0.0,6.0,0.0
E6,4.5,0.0,0.0,19.0,0.0,0.0,9.0,0.0,0.0,6.0,0.0,0.0,20.0,0.0,0.0,16.0,0.0,20.0,0.0
E7,13.5,0.0,0.0,5.5,0.0,0.0,0.0,11.0,0.0,18.0,0.0,0.0,14.5,0.0,0.0,13.0,0.0,4.0,0.0
E8,10.0,0.0,0.0,15.5,0.0,0.0,14.5,0.0,0.0,13.5,0.0,0.0,11.0,0.0,0.0,4.5,0.0,0.0,9.5
E9,0.0,8.5,0.0,6.0,0.0,0.0,15.0,0.0,0.0,13.5,0.0,0.0,9.5,0.0,0.0,4.0,0.0,7.5,0.0
E10,14.0,0.0,0.0,15.5,0.0,0.0,12.0,0.0,0.0,8.5,0.0,0.0,17.0,0.0,0.0,15.5,0.0,10.0,0.0
E11,15.0,0.0,0.0,15.0,0.0,0.0,0.0,20.0,0.0,0.0,5.5,0.0,6.5,0.0,0.0,0.0,13.0,12.5,0.0
E12,0.0,13.0,0.0,18.0,0.0,0.0,11.0,0.0,0.0,17.0,0.0,0.0,11.5,0.0,0.0,12.5,0.0,7.0,0.0
F1,11.0,0.0,0.0,11.5,0.0,0.0,15.5,0.0,0.0,6.5,0.0,0.0,14.0,0.0,0.0,13.0,0.0,5.5,0.0
F2,7.5,0.0,0.0,8.5,0.0,0.0,18.0,0.0,0.0,19.5,0.0,0.0,17.5,0.0,0.0,8.5,0.0,6.5,0.0
F3,6.0,0.0,0.0,4.0,0.0,0.0,5.5,0.0,0.0,10.5,0.0,0.0,14.0,0.0,0.0,16.0,0.0,16.5,0.0
F4,17.0,0.0,0.0,0.0,5.5,0.0,17.0,0.0,0.0,6.0,0.0,0.0,20.0,0.0,0.0,15.0,0.0,0.0,11.5
F5,18.0,0.0,0.0,10.5,0.0,0.0,5.5,0.0,0.0,6.5,0.0,0.0,11.5,0.0,0.0,17.5,0.0,17.5,0.0
F6,19.0,0.0,0.0,0.0,12.5,0.0,7.5,0.0,0.0,18.5,0.0,0.0,16.5,0.0,0.0,19.5,0.0,0.0,4.5
F7,14.0,0.0,0.0,13.0,0.0,0.0,11.5,0.0,0.0,7.5,0.0,0.0,5.5,0.0,0.0,0.0,19.0,8.5,0.0
F8,7.0,0.0,0.0,0.0,14.5,0.0,10.0,0.0,0.0,17.5,0.0,0.0,17.5,0.0,0.0,5.0,0.0,18.0,0.0
F9,4.5,0.0,0.0,11.5,0.0,0.0,5.5,0.0,0.0,13.5,0.0,0.0,10.0,0.0,0.0,11.5,0.0,7.5,0.0
F10,8.0,0.0,0.0,17.5,0.0,0.0,8.5,0.0,0.0,4.5,0.0,0.0,0.0,0.0,8.5,13.0,0.0,8.5,0.0
F11,9.0,0.0,0.0,7.5,0.0,0.0,15.5,0.0,0.0,5.5,0.0,0.0,6.5,0.0,0.0,19.5,0.0,8.5,0.0
F12,7.5,0.0,0.0,0.0,4.0,0.0,10.0,0.0,0.0,17.0,0.0,0.0,0.0,17.5,0.0,19.5,0.0,0.0,4.0
G1,13.0,0.0,0.0,9.0,0.0,0.0,12.5,0.0,0.0,16.5,0.0,0.0,15.5,0.0,0.0,15.5,0.0,11.5,0.0
G2,17.0,0.0,0.0,19.5,0.0,0.0,0.0,13.5,0.0,9.5,0.0,0.0,0.0,8.0,0.0,7.0,0.0,18.0,0.0
G3,13.0,0.0,0.0,0.0,0.0,18.0,5.5,0.0,0.0,0.0,0.0,0.5,13.5,0.0,0.0,6.0,0.0,14.0,0.0
G4,0.0,19.5,0.0,4.0,0.0,0.0,16.0,0.0,0.0,18.5,0.0,0.0,15.0,0.0,0.0,8.5,0.0,11.0,0.0
G5,0.0,6.0,0.0,16.0,0.0,0.0,4.0,0.0,0.0,4.0,0.0,0.0,14.5,0.0,0.0,18.5,0.0,19.5,0.0
G6,9.0,0.0,0.0,16.5,0.0,0.0,16.0,0.0,0.0,19.5,0.0,0.0,4.5,0.0,0.0,7.5,0.0,5.0,0.0
G7,14.5,0.0,0.0,0.0,13.0,0.0,10.0,0.0,0.0,12.5,0.0,0.0,13.0,0.0,0.0,8.5,0.0,18.5,0.0
G8,9.5,0.0,0.0,15.0,0.0,0.0,16.0,0.0,0.0,5.5,0.0,0.0,8.0,0.0,0.0,10.5,0.0,0.0,7.0
G9,14.5,0.0,0.0,9.0,0.0,0.0,8.5,0.0,0.0,5.0,0.0,0.0,9.0,0.0,0.0,17.5,0.0,15.0,0.0
G10,13.0,0.0,0.0,20.0,0.0,0.0,9.0,0.0,0.0,11.0,0.0,0.0,7.0,0.0,0.0,12.5,0.0,0.0,15.0
G11,0.0,0.0,6.0,12.0,0.0,0.0,15.0,0.0,0.0,10.5,0.0,0.0,7.0,0.0,0.0,0.0,18.0,20.0,0.0
G12,0.0,6.5,0.0,0.0,6.0,0.0,18.5,0.0,0.0,15.5,0.0,0.0,4.5,0.0,0.0,14.5,0.0,16.5,0.0
H1,15.5,0.0,0.0,6.0,0.0,0.0,16.5,0.0,0.0,6.0,0.0,0.0,15.5,0.0,0.0,0.0,8.5,4.0,0.0
H2,9.0,0.0,0.0,14.0,0.0,0.0,12.0,0.0,0.0,9.0,0.0,0.0,7.0,0.0,0.0,0.0,15.5,8.0,0.0
H3,17.0,0.0,0.0,0.0,19.0,0.0,0.0,7.0,0.0,14.5,0.0,0.0,5.5,0.0,0.0,0.0,3.0,0.0,2.0
H4,0.0,14.5,0.0,11.0,0.0,0.0,5.5,0.0,0.0,10.5,0.0,0.0,14.5,0.0,0.0,18.5,0.0,17.0,0.0
H5,19.5,0.0,0.0,7.0,0.0,0.0,16.5,0.0,0.0,6.0,0.0,0.0,12.5,0.0,0.0,13.5,0.0,12.5,0.0
H6,7.5,0.0,0.0,13.0,0.0,0.0,0.0,0.0,8.5,16.5,0.0,0.0,14.0,0.0,0.0,6.0,0.0,0.0,8.5
H7,0.0,13.5,0.0,13.5,0.0,0.0,13.5,0.0,0.0,9.0,0.0,0.0,13.5,0.0,0.0,16.5,0.0,0.0,12.5
H8,16.0,0.0,0.0,15.0,0.0,0.0,12.5,0.0,0.0,5.0,0.0,0.0,10.5,0.0,0.0,9.5,0.0,13.5,0.0
H9,15.0,0.0,0.0,13.5,0.0,0.0,19.0,0.0,0.0,16.5,0.0,0.0,0.0,0.0,14.5,14.0,0.0,9.0,0.0
H10,9.5,0.0,0.0,8.0,0.0,0.0,15.5,0.0,0.0,17.5,0.0,0.0,0.0,11.5,0.0,11.0,0.0,10.5,0.0
H11,4.5,0.0,0.0,5.0,0.0,0.0,4.5,0.0,0.0,17.5,0.0,0.0,13.0,0.0,0.0,5.0,0.0,10.5,0.0
H12,10.0,0.0,0.0,0.0,0.0,10.5,0.0,9.5,0.0,13.0,0.0,0.0,9.0,0.0,0.0,0.0,16.5,8.0,0.0
'''

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_20ul', 8)
	reservoir = protocol.load_labware('corning_24_wellplate_3.4ml_flat', 4)
	plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 2)
	p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tiprack])
	
	EXCEL_DATA = pd.read_csv(StringIO(DATA))
	for STOCK in EXCEL_DATA.columns[1:]:
		p20.pick_up_tip()
		for index, row in EXCEL_DATA.iterrows():
			volume = row[STOCK]  # Extract the volume for the current well
			destination_wells = list(EXCEL_DATA.iloc[:, 0])  # Extract the destination well name

			if pd.notnull(volume) and volume != 0:  # Check if the volume is not None or zero
				source_well = reservoir.wells_by_name()[STOCK]
				for WELL in destination_wells:
					destination_well = plate.wells_by_name()[WELL]
					p20.transfer(float(volume), source_well, destination_well.bottom(5), new_tip='never', touch_tip=True)
		p20.drop_tip()