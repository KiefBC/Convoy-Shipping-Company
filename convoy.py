import csv
import re
import pandas as pd


class Convoy:
    """I don't know yet"""

    def __init__(self, filename):
        self.convoy_filename = filename

    def clean_csv(self):
        count = 0
        cells = 0
        checked_csv = f'{self.convoy_filename[:-4]}[CHECKED].csv'
        with open(self.convoy_filename, 'r') as csv_file:
            with open(f'{checked_csv}', 'w') as cleaned_file:
                file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
                file_writer = csv.writer(cleaned_file, delimiter=',', lineterminator='\n')
                for row in file_reader:
                    if count == 0:
                        file_writer.writerow(row)
                        count += 1
                    else:
                        new_list = []
                        for elem in row:
                            if elem.isdigit():
                                new_list.append(elem)
                            else:
                                # Using regex to remove all non-alphanumeric characters
                                cleaned_elem = re.sub(r'\D', '', elem)
                                cells += 1
                                new_list.append(cleaned_elem)
                        file_writer.writerow(new_list)
            print(f'{cells} {"cells were" if cells > 1 else "cell was"} corrected in {checked_csv}')

    def convert_xlsx(self, filename):
        the_dataframe = pd.read_excel(filename, sheet_name='Vehicles', engine='openpyxl', dtype=str)
        self.convoy_filename = filename[:-5] + '.csv'
        the_dataframe.to_csv(f'{self.convoy_filename}', index=False, header=True)
        print(f"{the_dataframe.shape[0]} {'lines were' if the_dataframe.shape[0] > 1 else 'line was'} added to {self.convoy_filename}")


def main():
    # while True:
    try:
        filename = input('Input file name: ')
        if not re.match(".*\.(csv|xlsx)", filename):
            print('Make sure you only use .xlsx or .csv extension files\n')
    except FileNotFoundError as e:
        print(f'\nFile {e} not found')

    convoy = Convoy(filename)
    if re.match(".*\.(xlsx)$", filename):
        # If the file is an Excel file, convert it to csv
        convoy.convert_xlsx(filename)
        # Then clean the csv file
        convoy.clean_csv()
            # break


if __name__ == '__main__':
    main()
