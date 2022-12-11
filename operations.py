import json
import re
import sqlite3
import csv

import pandas as pd
from lxml import etree


class Convoy:

    def __init__(self, filename: str) -> None:
        self.db = f'{filename}.s3db'
        self.conn = sqlite3.connect(f'{filename}.s3db')
        self.cursor = self.conn.cursor()

    def clean_csv(self, filename: str) -> None:
        """
        This function cleans a CSV file
        :param filename:
        :return:
        """
        # Preparing our Counter and Cell Counter
        counter = 0
        num_cells = 0

        # Rename the file to [CHECKED].csv
        checked_csv = f'{filename}[CHECKED].csv'
        # Add CSV extension to the filename
        filename = f'{filename}.csv'
        with open(filename, 'r') as csv_file:
            with open(checked_csv, 'w') as cleaned_file:
                # Read the Original CSV File and Write in the new CSV File
                file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
                file_writer = csv.writer(cleaned_file, delimiter=',', lineterminator='\n')
                for row in file_reader:
                    # if Count = 0 then Header
                    if counter == 0:
                        file_writer.writerow(row)
                        counter += 1
                    # If not the header
                    else:
                        new_list = []
                        for cell in row:
                            # If the cell contains digits only
                            if cell.isdigit():
                                new_list.append(cell)
                            else:
                                # Using regex to remove all non-alphanumeric characters
                                cleaned_cell = re.sub(r'\D', '', cell)
                                num_cells += 1
                                new_list.append(cleaned_cell)
                        file_writer.writerow(new_list)
            # Announce the number of cells that were corrected
            print(f'{num_cells} {"cells were" if num_cells > 1 else "cell was"} corrected in {checked_csv}')

    def convert_xlsx_to_csv(self, filename: str) -> None:
        """
        This function converts an Excel file to a CSV file
        :param filename:
        :return:
        """
        # New CSV filename
        new_csv = f'{filename}.csv'
        # Add XLSX extension to the filename
        filename = f'{filename}.xlsx'
        # Read the file and convert it to a dataframe using pandas
        df = pd.read_excel(filename, sheet_name='Vehicles', engine='openpyxl', dtype=str)
        # Convert to CSV
        df.to_csv(new_csv, index=False, header=True)
        # Count the number of rows added
        rows = df.shape[0]
        print(f'{rows} line{"s were" if rows != 1 else " was"} added to {new_csv}')

    def convert_sqlite_to_json(self, filename: str) -> None:
        """
        This function converts a SQLite database to a JSON file
        :param filename:
        :return:
        """
        if '[CHECKED]' in filename:
            filename = filename.replace('[CHECKED]', '')
        else:
            filename = filename
        # New JSON filename
        new_json = f'{filename}.json'
        df = pd.read_sql_query('SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load'
                               ' FROM convoy'
                               ' WHERE score > 3', self.conn)
        # Create a Dictionary from the DataFrame
        data = df.to_dict(orient='records')
        convoy_dict = {'convoy': data}
        # Create a JSON file
        with open(new_json, 'w') as json_file:
            json.dump(convoy_dict, json_file, indent=4)
        # Count the number of rows added, and announce it
        rows = df.shape[0]
        print(f'{rows} vehicle{"s were" if rows != 1 else " was"} saved into {new_json}')

    def convert_to_xml(self, filename: str):
        """
        This function converts a JSON file to an XML file
        :param filename:
        :return:
        """
        # XML Filename
        new_xml = f'{filename}.xml'
        # XML String
        string = '<convoy>'
        # Read the file and convert it to a dataframe using pandas
        df = pd.read_sql_query('SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load'
                               ' FROM convoy'
                               ' WHERE score <= 3', self.conn)
        for x in range(len(df)):
            string += f'\n\t<vehicle>\n\t\t<vehicle_id>{df.vehicle_id[x]}</vehicle_id>' \
                      f'\n\t\t<engine_capacity>{df.engine_capacity[x]}</engine_capacity>' \
                      f'\n\t\t<fuel_consumption>{df.fuel_consumption[x]}</fuel_consumption>' \
                      f'\n\t\t<maximum_load>{df.maximum_load[x]}</maximum_load>' \
                      f'\n\t</vehicle>'
        string += '\n</convoy>'
        # Create a XML file
        root = etree.fromstring(string)
        root.getroottree().write(new_xml, pretty_print=True)
        # Announce the number of rows added
        length = len(df)
        print(f'{length} vehicle{"s were" if length != 1 else " was"} saved into {new_xml}')

    def the_score(self, capacity: int, consumption: int, maximum_load: int) -> int:
        """
        This function calculates the score of a vehicle
        :param capacity:
        :param consumption:
        :param maximum_load:
        :return:
        """
        score = 0
        pit_stops = 4.5 // (capacity / consumption)
        if pit_stops == 0:
            score += 2
        else:
            score += 1
        if maximum_load >= 20:
            score += 2
        if consumption * 4.5 <= 230:
            score += 2
        else:
            score += 1
        return score
