import pandas as pd

"""stuff 2 do"""

default = 'convoy.xlsx'

file_input = input('Input file name:\n') or default
my_df = pd.read_excel(f'{file_input}', sheet_name='Vehicles', dtype=str)
my_df.to_csv(f'{file_input.replace(".xlsx", ".csv")}', index=False)
my_df = pd.read_csv(f'{file_input.replace(".xlsx", ".csv")}', dtype=str)

if int(my_df.shape[0]) <= 1:
    print(f'{my_df.shape[0]} line was imported to {file_input.replace(".xlsx", ".csv")}')
else:
    print(f'{my_df.shape[0]} lines were imported to {file_input.replace(".xlsx", ".csv")}')