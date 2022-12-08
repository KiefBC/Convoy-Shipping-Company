import json
import re
import sqlite3
import csv
import pandas as pd


class Convoy:

    def __init__(self) -> None:
        pass

    def clean_csv(self, filename):
        # Preparing our Counter and Cell Counter
        counter = 0
        num_cells = 0

        # Rename the file to [CHECKED].csv
        # checked_csv = f'{filename[:-4]}[CHECKED].csv'
        checked_csv = f'{filename}[CHECKED].csv'

        # Add CSV extension to the filename
        filename = f'{filename}.csv'

        # Open the file
        with open(filename, 'r') as csv_file:
            with open(checked_csv, 'w') as cleaned_file:

                # Read the Original CSV File and Write in the new CSV File
                file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
                file_writer = csv.writer(cleaned_file, delimiter=',', lineterminator='\n')

                # Loop through the rows
                for row in file_reader:

                    # if Count = 0 then Header
                    if counter == 0:
                        file_writer.writerow(row)
                        counter += 1

                    # If not the header
                    else:
                        new_list = []

                        # Loop through the cells
                        for cell in row:

                            # If the cell contains digits only
                            if cell.isdigit():
                                new_list.append(cell)

                            # If the cell contains non-digits
                            else:
                                # Using regex to remove all non-alphanumeric characters
                                cleaned_cell = re.sub(r'\D', '', cell)
                                num_cells += 1
                                new_list.append(cleaned_cell)

                        # Write the new row
                        file_writer.writerow(new_list)

            # Announce the number of cells that were corrected
            print(f'{num_cells} {"cells were" if num_cells > 1 else "cell was"} corrected in {checked_csv}')

    def convert_xlsx_to_csv(self, filename):
        # New CSV filename
        # new_csv = filename[:-5] + '.csv'
        new_csv = f'{filename}.csv'

        # Add xlsx extension to the filename
        filename = f'{filename}.xlsx'

        # Read the file and convert it to a dataframe using pandas
        df = pd.read_excel(filename, sheet_name='Vehicles', engine='openpyxl', dtype=str)

        # Convert to CSV
        df.to_csv(new_csv, index=False, header=True)

        rows = df.shape[0]
        print(f'{rows} line{"s were" if rows != 1 else " was"} added to {new_csv}')

    def convert_sqlite_to_json(self, filename):
        # New JSON filename
        new_json = f'{filename}.json'

        # Add s3db extension to the filename
        filename = f'{filename}.s3db'

        # Connect to the database
        conn = sqlite3.connect(filename)

        # Create a cursor
        df = pd.read_sql_query('SELECT * FROM convoy', conn)
        # Create a Dictionary from the DataFrame
        data = df.to_dict(orient='records')
        convoy_dict = {'convoy': data}
        # Create a JSON file
        with open(new_json, 'w') as json_file:
            json.dump(convoy_dict, json_file, indent=4)

        rows = df.shape[0]
        print(f'{rows} vehicle{"s were" if rows != 1 else " was"} saved into {new_json}')
