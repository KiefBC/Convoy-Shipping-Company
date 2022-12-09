import json
import re
import sqlite3
import csv
from dicttoxml import dicttoxml
from pprint import pprint

import pandas as pd
from lxml import etree


class Convoy:

    def __init__(self, filename) -> None:
        self.db = f'{filename}.s3db'
        self.conn = sqlite3.connect(f'{filename}.s3db')
        self.cursor = self.conn.cursor()

    def clean_csv(self, filename: str) -> None:
        """
        This function cleans a CSV file
        :param filename:
        :return:
        """
        counter = 0
        num_cells = 0
        # Rename the file to [CHECKED].csv
        checked_csv = f'{filename}[CHECKED].csv'
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
            print(f'{num_cells} {"cells were" if num_cells > 1 else "cell was"} corrected in {checked_csv}')

    def convert_xlsx_to_csv(self, filename: str) -> None:
        """
        This function converts an Excel file to a CSV file
        :param filename:
        :return:
        """
        new_csv = f'{filename}.csv'
        filename = f'{filename}.xlsx'
        df = pd.read_excel(filename, sheet_name='Vehicles', engine='openpyxl', dtype=str)
        df.to_csv(new_csv, index=False, header=True)
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
        new_json = f'{filename}.json'
        df = pd.read_sql_query('SELECT * FROM convoy', self.conn)
        data = df.to_dict(orient='records')
        convoy_dict = {'convoy': data}
        with open(new_json, 'w') as json_file:
            json.dump(convoy_dict, json_file, indent=4)
        rows = df.shape[0]
        print(f'{rows} vehicle{"s were" if rows != 1 else " was"} saved into {new_json}')

    def convert_to_xml(self, filename):
        """
        This function converts a JSON file to an XML file
        :param filename:
        :return:
        """
        new_xml = f'{filename}.xml'
        df = pd.read_sql_query('SELECT * FROM convoy', self.conn)
        xml_result = df.to_xml(root_name='convoy', row_name='vehicle', xml_declaration=False, index=False)
        with open(new_xml, 'w') as xml_file:
            xml_file.write(xml_result)
        length = len(df)
        print(f'{length} vehicle{"s were" if length != 1 else " was"} saved into {new_xml}')

