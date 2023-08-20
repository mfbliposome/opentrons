# This file contains the coding logic for various protocols that, when run, will generate 
# an OpenTron input file to be uploaded by the OpenTron GUI

class Distribute_Dilution:
    def __init__(self, DATA) -> None:
        # Protocol Metadata
        self.METADATA = {
            'apiLevel': '2.13',
            'protocolName': 'Distribute_Dilution',
            'description': '''This protocol is a modified version of the Serial_Dilution_Tutorial''',
            'author': 'New API User'
            }
        
        # String Data obtained from an Excel Workbook
        self.DATA = DATA

        # Instructions to be carried out by the OpenTron robot
        # Modify this section to alter the robotic arm's behavior using built-in opentron functions
        RESERVIOR = DATA.partition(",")[0] # Obtain the column name for the first column, which contains the destination wells
        self.INSTRUCTIONS = (
            f"\tEXCEL_DATA = pd.read_csv(StringIO(DATA))\n"
            f"\tfor STOCK in EXCEL_DATA.columns[1:]:\n"
            f"\t\tp300.pick_up_tip()\n"
            f"\t\tp300.distribute(list(EXCEL_DATA[STOCK]), STOCK, list(EXCEL_DATA['{RESERVIOR}']))\n"
            f"\t\tp300.drop_tip()\n"
            )        

    def generate_imports(self):
        return (
            f"# Upload this data/instructions file via the OpenTrons GUI\n"
            f"import pandas as pd\n"
            f"from io import StringIO\n"
            f"from opentrons import protocol_api\n\n"
            f"METADATA = {self.METADATA}\n\n"
        )

    def generate_data(self):
        return (
            f"DATA = '''\n"
            f"{self.DATA}'''\n\n"
        )

    def generate_run(self):
        return (
            f"def run(protocol: protocol_api.ProtocolContext):\n"
            f"\ttiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 8)\n"
            f"\tp300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack])\n"
            f"{self.INSTRUCTIONS}"
        )

    # Generates the input file when run
    def input_file_generator(self):
        return (
            f"{self.generate_imports()}"
            f"{self.generate_data()}"
            f"{self.generate_run()}"
        )

class Serial_Dilution_Tutorial:
    def __init__(self, DATA) -> None:
        # Protocol Metadata
        self.METADATA = {
            'apiLevel': '2.13',
            'protocolName': 'Serial Dilution Tutorial',
            'description': '''This protocol is the outcome of following the Python Protocol API Tutorial located at https://docs.opentrons.com/v2/tutorial.html. It takes a solution and progressively dilutes it by transferring it stepwise across a plate.''',
            'author': 'New API User'
            }
        
        # String Data obtained from an Excel Workbook
        self.DATA = DATA

        # Instructions to be carried out by the OpenTron robot
        # Modify this section to alter the robotic arm's behavior using built-in opentron functions
        RESERVIOR = DATA.partition(",")[0] # Obtain the column name for the first column, which contains the destination wells
        self.INSTRUCTIONS = (
            f"\tEXCEL_DATA = pd.read_csv(StringIO(DATA))\n"
            f"\tfor STOCK in EXCEL_DATA.columns[1:]:\n"
            f"\t\tp300.pick_up_tip()\n"
            f"\t\tp300.distribute(list(EXCEL_DATA[STOCK]), STOCK, list(EXCEL_DATA['{RESERVIOR}']))\n"
            f"\t\tp300.drop_tip()\n"
            )        

    def generate_imports(self):
        return (
            f"# Upload this data/instructions file via the OpenTrons GUI\n"
            f"import pandas as pd\n"
            f"from io import StringIO\n"
            f"from opentrons import protocol_api\n\n"
            f"METADATA = {self.METADATA}\n\n"
        )

    def generate_data(self):
        return (
            f"DATA = '''\n"
            f"{self.DATA}'''\n\n"
        )

    def generate_run(self):
        return (
            f"def run(protocol: protocol_api.ProtocolContext):\n"
            f"\ttips = protocol.load_labware('opentrons_96_tiprack_300ul', 1)\n"
            f"\treservoir = protocol.load_labware('nest_12_reservoir_15ml', 2)\n"
            f"\tplate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)\n"
            f"\tleft_pipette = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tips])\n\n"
            f"\t# distribute diluent\n"
            f"\tleft_pipette.transfer(100, reservoir['A1'], plate.wells())\n\n"
            f"\t# loop through each row"
            f"\tfor i in range(8):\n"
            f"\t\trow = plate.rows()[i] # save the destination row to a variable\n"
            f"\t\tleft_pipette.transfer(100, reservoir['A2'], row[0], mix_after=(3, 50)) # transfer solution to first well in column \n"
            f"\t\tleft_pipette.transfer(100, row[:11], row[1:], mix_after=(3, 50)) # dilute the sample down the row\n"
        )

    # Generates the input file when run
    def input_file_generator(self):
        return (
            f"{self.generate_imports()}"
            f"{self.generate_data()}"
            f"{self.generate_run()}"
        )