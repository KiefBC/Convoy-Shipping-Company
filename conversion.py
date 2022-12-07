import re
import csv
import pandas as pd


class Convoy:
    """
    I don't know yet
    """

    def __init__(self, filename: str) -> None:
        self.convoy_filename = filename

    def clean_csv(self, checking_csv) -> None:
        """
        Clean up the csv file
        :return: None
        """
        count = 0
        cells = 0
        checked_csv = f'{checking_csv[:-4]}[CHECKED].csv'
        with open(checking_csv, 'r') as csv_file:
            with open(f'{checked_csv}', 'w') as cleaned_file:
                # Read the Original CSV File, and Write in the new CSV File
                file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
                file_writer = csv.writer(cleaned_file, delimiter=',', lineterminator='\n')
                for row in file_reader:
                    # if Count = 0 then Header
                    if count == 0:
                        file_writer.writerow(row)
                        count += 1
                    else:
                        new_list = []
                        for elem in row:
                            # If the cell contains digits only
                            if elem.isdigit():
                                new_list.append(elem)
                            else:
                                # Using regex to remove all non-alphanumeric characters
                                cleaned_elem = re.sub(r'\D', '', elem)
                                cells += 1
                                new_list.append(cleaned_elem)
                        file_writer.writerow(new_list)
            print(f'{cells} {"cells were" if cells > 1 else "cell was"} corrected in {checked_csv}')

    def convert_xlsx(self, filename: str):
        """
        Convert xlsx file to csv
        :param filename:
        :return:
        """
        # Read in the file
        the_dataframe = pd.read_excel(filename, sheet_name='Vehicles', engine='openpyxl', dtype=str)
        self.convoy_filename = filename[:-5] + '.csv'
        # Write it out to a csv file
        the_dataframe.to_csv(f'{self.convoy_filename}', index=False, header=True)
        print(
            f"{the_dataframe.shape[0]} {'lines were' if the_dataframe.shape[0] > 1 else 'line was'} added to {self.convoy_filename}")
        self.clean_csv(self.convoy_filename)
