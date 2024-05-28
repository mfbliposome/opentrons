# Upload this data/instructions file via the OpenTrons GUI\n"
import pandas as pd
from io import StringIO
from opentrons import protocol_api

metadata = {
	'apiLevel': '2.13',
	'protocolName': 'Aphiphile_Dispensation', # protocolName should be same name as current file
	'description': '''
	This simple protocol transfers one stock solution to a series of destination wells for each stock solution in an excel workbook 
	''',
	'author': 'ER'
	}

# These Strings will be populated in 'opentron_input_files' after running 'main.py' (do not change!)
INSTRUCTIONS = """"""
LABWARE = """"""
PIPETTE = """"""

# Load instructions from excel workbook
def get_instructions_from(INSTRUCTIONS):
	INSTRUCT = pd.read_csv(StringIO(INSTRUCTIONS))
	DECK_SLOTS = INSTRUCT[INSTRUCT.columns[0]] # The first column has deck slot that indicate where the destination plates are located in the OT-2  
	slots = DECK_SLOTS.unique() # Get the slots numbers being used
	return INSTRUCT, slots

# Load labware for the experiment
def get_labware_from(LABWARE, protocol):
	LAB_W = pd.read_csv(StringIO(LABWARE))
	plates = []
	for i in range(len(LAB_W)):
		LABWARE_ROLE = LAB_W['ROLE'].iloc[i]
		if LABWARE_ROLE == "Destination_Wells":
			plates.append(protocol.load_labware(LAB_W['LABWARE_API_NAME'].iloc[i], int(LAB_W['LABWARE_DECK_SLOT'].iloc[i])))
		elif LABWARE_ROLE == "Stock_Solutions":
			reservoir = protocol.load_labware(LAB_W['LABWARE_API_NAME'].iloc[i], int(LAB_W['LABWARE_DECK_SLOT'].iloc[i]))
		elif LABWARE_ROLE == "Tips_Rack":
			tiprack = protocol.load_labware(LAB_W['LABWARE_API_NAME'].iloc[i], int(LAB_W['LABWARE_DECK_SLOT'].iloc[i]))
	return plates, reservoir, tiprack

# Load pipette and convert to labware object
def get_pipettes_from(PIPETTE, protocol, tiprack):
	PIPETTE_TYPE = pd.read_csv(StringIO(PIPETTE))
	PIPETTE_LOCATION = PIPETTE_TYPE[PIPETTE_TYPE.columns[0]][0]
	PIPETTE_API_NAME = PIPETTE_TYPE[PIPETTE_TYPE.columns[1]][0]
	pipette = protocol.load_instrument(PIPETTE_API_NAME, PIPETTE_LOCATION, tip_racks=[tiprack])
    
    # Change clearance height for aspiration/dispensation to 5 mm above the bottom of the well
	pipette.well_bottom_clearance.aspirate = 2
	pipette.well_bottom_clearance.dispense = 2
	return pipette

# Obtain the instruction set for a single deck slot and relevant variables
def filter_table_using(slots, deck_slot, INSTRUCT):
	INST = INSTRUCT[INSTRUCT[INSTRUCT.columns[0]] == slots[deck_slot]].reset_index().drop('index', axis=1)
	DESTINATIONS = list(INST[INST.columns[1]])                          # destination wells of the regeant
	SOLUTIONS = list(INST.columns[2:])                                  # locations of the stock solutions for dispensation
	return INST, DESTINATIONS, SOLUTIONS

# A simple aspirate, dispense, and blow out protocol
def custom_transfer_protocol(pipette, volume, from_stock_location, to_destination):
	pipette.aspirate(volume, from_stock_location)
	pipette.dispense(volume, to_destination)
	pipette.touch_tip(to_destination, speed = 15, radius = 0.75, v_offset = -3)
	pipette.blow_out()

def run(protocol: protocol_api.ProtocolContext):
	# Obtain protocol information variables
	INSTRUCT, slots = get_instructions_from(INSTRUCTIONS)
	plates, reservoir, tiprack = get_labware_from(LABWARE, protocol)
	p = get_pipettes_from(PIPETTE, protocol, tiprack)
	
    # Core protocol: Filter instruction table for plate number of interest before transfer
	for deck_slot in range(len(slots)):
		instructions, destinations, solutions = filter_table_using(slots, deck_slot, INSTRUCT)
		
        # Pick up a new tip for each stock solution and dispense when complete
		num_dispensations = len(instructions)
		for stock in solutions:
			p.pick_up_tip()
			
            # Aspirate a stock solution and dispense into a destination well of interest
			for i in range(num_dispensations):
				# Set up variables
				volume = instructions[stock].iloc[i]
				well = destinations[i]
				from_stock_location = reservoir[stock]# plate[deck_slot][stock]
				to_destination = plates[deck_slot][well]
				
                # Skip transfer call if there is no volume to be transfered
				if volume == 0.0: continue
				
                # Transfer call
				custom_transfer_protocol(p, volume, from_stock_location, to_destination)
				
			p.drop_tip()
