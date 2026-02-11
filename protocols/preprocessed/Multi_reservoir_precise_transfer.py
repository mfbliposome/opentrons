# Upload this data/instructions file via the OpenTrons GUI\n"
import pandas as pd
from io import StringIO
from opentrons import protocol_api

metadata = {
	'apiLevel': '2.13',
	'protocolName': 'Multiple reservoirs', # protocolName should be same name as current file
	'description': '''
	This simple protocol transfers stock solutions from multiples reservoirs to a series of destination wells for each stock solution in an excel workbook 
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
	slots = sorted(DECK_SLOTS.unique()) # Get the slots numbers being used
	return INSTRUCT, slots

# Load labware for the experiment
def get_labware_from(LABWARE, protocol):
	LAB_W = pd.read_csv(StringIO(LABWARE))
	plates = {}
	reservoirs = {}
	tipracks = []
    
	for i in range(len(LAB_W)):
		LABWARE_ROLE = LAB_W['ROLE'].iloc[i]
		API_NAME = LAB_W['LABWARE_API_NAME'].iloc[i]
		SLOT = int(LAB_W['LABWARE_DECK_SLOT'].iloc[i])
		if LABWARE_ROLE == "Destination_Wells":
			plates[SLOT] = protocol.load_labware(API_NAME, SLOT)
		elif LABWARE_ROLE == "Stock_Solutions":
			reservoirs[SLOT] = protocol.load_labware(API_NAME, SLOT)
		elif LABWARE_ROLE == "Tips_Rack":
			tipracks.append(protocol.load_labware(API_NAME, SLOT))
	return plates, reservoirs, tipracks

												  
# Build the resevoir map												  
def build_res_map(LABWARE):
	LAB_W = pd.read_csv(StringIO(LABWARE))
	res_map = {}
	res_count = 0
	for i in range(len(LAB_W)):
		if LAB_W['ROLE'].iloc[i] == "Stock_Solutions":
			slot = int(LAB_W['LABWARE_DECK_SLOT'].iloc[i])
			res_map[f"RES{res_count}"] = slot
			res_count += 1
	return res_map

# Load pipette and convert to labware object
def get_pipettes_from(PIPETTE, protocol, tipracks):
	PIPETTE_TYPE = pd.read_csv(StringIO(PIPETTE))
	PIPETTE_LOCATION = PIPETTE_TYPE[PIPETTE_TYPE.columns[0]][0]
	PIPETTE_API_NAME = PIPETTE_TYPE[PIPETTE_TYPE.columns[1]][0]
	pipette = protocol.load_instrument(PIPETTE_API_NAME, PIPETTE_LOCATION, tip_racks=tipracks)
    
    # Change clearance height for aspiration/dispensation to 3 mm above the bottom of the well
	pipette.well_bottom_clearance.aspirate = 3
	pipette.well_bottom_clearance.dispense = 3
	
	# Set custom flow rates: Change these numbers according to the pipette you are using (ie:used 10-15ul for p20 and 160-200ul for p300)
	#pipette.flow_rate.aspirate = 15   
	#pipette.flow_rate.dispense = 15
	#pipette.flow_rate.blow_out = 15
	return pipette

# Obtain the instruction set for a single deck slot and relevant variables
def filter_table_using(deck_slot, INSTRUCT):
	INST = INSTRUCT[INSTRUCT[INSTRUCT.columns[0]] == deck_slot].reset_index(drop=True)
	DESTINATIONS = list(INST[INST.columns[1]])                          # destination wells of the regeant
	SOLUTIONS = list(INST.columns[2:])                                  # locations of the stock solutions for dispensation
	return INST, DESTINATIONS, SOLUTIONS

# A simple aspirate, dispense, and blow out protocol
def custom_transfer_protocol(pipette, volume, from_stock_location, to_destination):
	pipette.aspirate(volume, from_stock_location)
	pipette.dispense(volume, to_destination)
	pipette.touch_tip(to_destination, speed=15,radius =0.75, v_offset = -3)
	pipette.blow_out()

def run(protocol: protocol_api.ProtocolContext):
	# Obtain protocol information variables
	INSTRUCT, slots = get_instructions_from(INSTRUCTIONS)
	plates, reservoirs, tipracks = get_labware_from(LABWARE, protocol)
	p = get_pipettes_from(PIPETTE, protocol, tipracks)
	res_map = build_res_map(LABWARE)
	
    # Core protocol: Filter instruction table for plate number of interest before transfer
	for deck_slot in slots:
		instructions, destinations, solutions = filter_table_using(deck_slot, INSTRUCT)
		
        # Pick up a new tip for each stock solution and dispense when complete
		num_dispensations = len(instructions)
		for stock in solutions:
			res_label, res_well = stock.split(":")
			res_slot = res_map[res_label]
			reservoir = reservoirs[res_slot]
			if instructions[stock].sum() == 0:
			    continue
			
			p.pick_up_tip()
			
            # Aspirate a stock solution and dispense into a destination well of interest
			for i in range(num_dispensations):
				# Set up variables
				volume = instructions[stock].iloc[i]
				well = destinations[i]
				from_stock_location = reservoir[res_well]# plate[deck_slot][stock]
				to_destination = plates[deck_slot][well]
				
                # Skip transfer call if there is no volume to be transfered
				if volume == 0.0: continue
				
                # Transfer call
				custom_transfer_protocol(p, volume, from_stock_location, to_destination)
				
			p.drop_tip()



