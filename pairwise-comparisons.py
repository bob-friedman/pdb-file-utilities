# python3 code to print list of all pairs of files
#  in a directory. Does not include pairs of the same
#  file. List is unordered.

# adaptable for creating a shell script for automation:
#  print(f"python TMscore.exe {file1} {file2}")

# modify directory name below

import os
from itertools import combinations

def pairwise_comparisons(directory):
    files = os.listdir(directory)
    for file1, file2 in combinations(files, 2):
        # print list of all pairs of files
        print(f"{file1} {file2}")

# modify directory to the files of interest
directory = 'C:/Peptide3d/data'
pairwise_comparisons(directory)
