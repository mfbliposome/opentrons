# Automated Experimentation
Repo for programming the automated liquid handler [OpenTrons](https://docs.opentrons.com/v2/index.html) 

## Directions

The OT-2 robot requires a Python input file to carry out experiments. Given a `.xlsx` tabular data file (in `./data/`) and a `.py` instruction sheet (in `./protocols/preprocessed`), `main.py` will convert your data to a `String` and write a new `.py` file. This Python file is set to output in `./protocols/postprocessed` and contains both your original instruction logic and data. Upload this file to the OpenTrons GUI to have the OT-2 robot carry out your experiment. Consider this example workflow:

1. `Clone` this repository to your computer in a directory of interest
1. Run `pip install -r requirements.txt` 
1. Create a **Data** file for your experiment, located in `/data/`
1. Create an intruction **Protocol** for the OT-2 robot, located in `/protocol/preprocessed/`
1. Open a command-line terminal and run the command `python main.py` and follow the input prompts. The **Simulator** output reflects the behavior OT-2 when following your protocol
1. Use the resulting **Input File**, located in `/protocol/postprocessed`, by uploading the new file to OpenTron 

### Protocols

The OT-2 robot requires data to be accepted in the form of a `String`. To satisfy this requirment while providing user flexibility for creating data files in another format (in this case, Microsoft Excel), the `./protocols` directory contains two subdirectories. The `/preprocessed/` directory contains OT-2 `.py` instruction files. After running `main.py`, the `input_file_generator()` in `/preprocessed/utils/file_converter.py` will create a new `.py` file in `./protocols/postprocessed/` with a data `String` included. This is done by replacing one line of code in the `/preprocessed/` file:

```
DATA = """""" #
```

Make sure this line of code is included when creating new `.py` files. Only use files in `/postprocessed/` as input files for the OpenTron GUI.

### Data Organization

The `./protocols/utils/file_conversion.py` functions assume that the `.xlsx` data file contains two sheets. `Sheet1` contains information pertaining to the reagents, destination, and volume number of reagent to be transfered. The first column should contain `String` locations for the destination wells and each following column should contain `float` volumes for each reagent to be transfered. For example:

| Well | Reagent1 | Reagent2 |
|-----:|-----------|-----------|
|     A1|     40|     20|
|     A2|     20|     50|
|     A3|     60|     10|
|    ...|    ...|    ...|

`Sheet2` contains additional information regarding each reagent. Column 0 contains a `String` of reagent names, such that each row contains information pertaining to a reagent listed in the headers from `Sheet1`. Column 2 should contain the well location of each reagent. The data does not have to be set to these specific columns as long as the `data_converter()` parameters are adjusted in `./protocols/utils/file_conversion.py`. An example of how `Sheet2` can look like is the following:

|  | Reagent1 | Reagent2 |
|-----:|-----------|-----------|
|     Reagent1|     decanol|     A1|
|     Reagent2|     ethanol|     A2|
|    ...|    ...|    ...|