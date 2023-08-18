# python3 code to reset residue number value to 1
#  for the PDB formatted files created by pdb-split-files.py

import os

directory = 'C:/Peptide3d/data'
files = os.listdir(directory)

for file in files:
    if file.endswith('pdb'):
        print(file)
        pdb_file = file

        with open(pdb_file, 'r') as f:
            lines = f.readlines()

        current_residue = None
        start_residue = 1
        current_residue_number = start_residue - 1
    
        for i, line in enumerate(lines):
            if line.startswith('ATOM'):
                residue = line[22:26]
                if residue != current_residue:
                    current_residue = residue
                    current_residue_number += 1
                lines[i] = line[:22] + str(current_residue_number).rjust(4) \
                 + line[26:]
                
            if line.startswith('TER'):
                residue = line[22:26]
                if residue != current_residue:
                    current_residue = residue
                lines[i] = line[:22] + \
                 str(current_residue_number).rjust(4) + line[26:]

        with open(pdb_file, 'w') as f:
            f.writelines(lines)
