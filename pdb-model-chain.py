# python3 code to print the model and protein chain
#  for a directory of PDB formatted files with
#  extension name "pdb" (.pdb)

import glob
from Bio.PDB.PDBParser import PDBParser

# assign functions
parser = PDBParser()

# input file
for file in glob.glob('./*.pdb'):
    print("file: ", file)

    # retrieve PDB structure
    structure = parser.get_structure(file, file)

    # iterate over models and chains in file
    for model in structure:
        print("model: ", model)
        for chain in model:
           print("chain: ", chain)

