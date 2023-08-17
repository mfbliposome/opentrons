from opentrons import protocol_api
import pandas as pd

# We're assumming the plate is a 'corning_96_wellplate_360ul_flat'

# TODOs
# Optimize the code so that the arm is aspirating as few times as possible
# Adjust the code so that the arm is not dispensing more liquid than it currently has in the tip!
	
MAX_ASP = 300 # maximum number of liquid capable of being aspirated

INSTRUCT_SHEET = pd.read_excel('./data/opentron template test example.xlsx')
INSTRUCT_SHEET = INSTRUCT_SHEET.fillna(0)
INSTRUCT_SHEET = INSTRUCT_SHEET.sort_values('A1', ascending=False)

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution Tutorial',
    'description': '''This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.''',
    'author': 'New API User'
    }

def run(protocol: protocol_api.ProtocolContext):
	tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)
	plate = protocol.load_labware('3dprt_50ml_2x3', 3)
	well1 = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
	p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])

	def distribute_decanol_using(INSTRUCT_SHEET):
		# SAFE_THRESHOLD=10
		asp_volume = 0
		# Iterates through every stock being used in the experiment
		for STOCK in INSTRUCT_SHEET.columns:
			if STOCK == "Well_Number": continue
			p300.pick_up_tip()
			# Iterates through every row in one stock solution
			for row in range(len(INSTRUCT_SHEET)):
				assert(INSTRUCT_SHEET[STOCK].iloc[row]<=290)
				if asp_volume <= INSTRUCT_SHEET[STOCK].iloc[row]+10:
					p300.aspirate(MAX_ASP, plate[STOCK])
					asp_volume = MAX_ASP
				p300.dispense(INSTRUCT_SHEET[STOCK].iloc[row], well1[INSTRUCT_SHEET["Well_Number"].iloc[row]])
				asp_volume -= INSTRUCT_SHEET[STOCK].iloc[row]
		p300.drop_tip()
		
		
	print(INSTRUCT_SHEET)
	distribute_decanol_using(INSTRUCT_SHEET)

		# save the destination row to a variable
		#row = plate.rows()[i]

		# transfer solution to first well in column
		#p300.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50))

		# dilute the sample down the row
		#p300.transfer(100, row[:11], row[1:], mix_after=(3, 50))
