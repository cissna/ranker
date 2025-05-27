"""
Should just be a small file that runs a CLI to quickly input/output from clipboard, spreadsheet formatting
"""
from pyperclip import copy, paste
from rankThingsByIndividualComparisons.comparer import Comparer

input("Once you are have your spreadsheet column copied, press enter")
text = paste()

comparer = Comparer(paste().strip().split('\n'))
output = comparer.minimal_compare()

copy('\n'.join(output))
