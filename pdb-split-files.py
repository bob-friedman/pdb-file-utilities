# python3 code to split a PDB formatted file (.pdb) into files
#  of 9 amino acid residues. May create a large number of
#  files, so carefully test before use.

# python pdb-split.py > stdout-batch-1.txt

# import modules
import os
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import PDBIO
from Bio.PDB.Dice import ChainSelector

# define an alias for modules
parser = PDBParser()
io = PDBIO()

# edit directory for location of PDB formatted files
directory = 'C:/Peptide3d/data'
files = os.listdir(directory)

# iterate over files in directory named above
for file in files:
    if file.endswith('pdb'):
        print(file)

        # set variables
        count = start = length = 0

        # input file
        file_prefix = os.path.splitext(file)[0]
        file = os.path.join(directory, file_prefix + '.pdb')

        # retrieve PDB structure
        structure = parser.get_structure(file, file)
        io.set_structure(structure)

        # iterate over models and chains in file
        for model in structure:
            print("model", model)
            for chain in model:
               print("chain", chain)
               chain_id = chain.get_id()
               length = len([_ for _ in chain.get_residues()])
               # iterate over all residues in the protein chain
               for residue in chain.get_residues():
                   start += 1
                   # detect when less than 9 residues are left in chain
                   if (start + 8 > length):
                       # exit loop since at end of the chain
                       break
                   for count in range(start, start + 8):
                       # write each subsequence to an unique file
                       selection = ChainSelector(chain_id, start, start + 8)
                       file_save = os.path.join(directory, file_prefix + '_' \
                         + str(start) + '.pdb')
                       io.save(file_save, selection)
