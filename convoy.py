import csv
import re
import database
import pandas as pd


class Convoy:
    """
    I don't know yet
    """

    def __init__(self, filename: str) -> None:
        self.convoy_filename = filename

    def clean_csv(self) -> None:
        """
        Clean up the csv file
        :return: None
        """
        count = 0
        cells = 0
        checked_csv = f'{self.convoy_filename[:-4]}[CHECKED].csv'
        with open(self.convoy_filename, 'r') as csv_file:
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

    def convert_xlsx(self, filename: str) -> None:
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


def main() -> None:
    """
    Main function
    :return: None
    """
    while True:
        try:
            filename = input('Input file name\n')
            if not re.match(".*\.(csv|xlsx)", filename):
                print('Make sure you only use .xlsx or .csv extension files\n')
        except FileNotFoundError as e:
            print(f'\nERROR! {e}\n')
        else:
            # Removing the extension from the filename
            no_ext_file = filename[:-5] if filename.endswith('.xlsx') else filename[:-4]
            cv_db = database.Database(no_ext_file)
            # Establishing connection to the Class
            convoy = Convoy(filename)
            # cv_db.initialize_database()
            if re.match(".*\.(xlsx)$", filename):
                # If the file is an Excel file, convert it to csv
                convoy.convert_xlsx(filename)
                # Then clean the csv file
                convoy.clean_csv()
            else:
                # If the file is a csv file, clean it
                convoy.clean_csv()
            cleaned_csv = f'{convoy.convoy_filename[:-4]}[CHECKED].csv'
            count = 0
            # Insert the data into the database
            with open(cleaned_csv, 'r') as csv_file:
                file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
                # Skip the header
                next(file_reader)
                for row in file_reader:
                    # Insert the data into the database
                    cv_db.add_vehicle(int(row[0]), int(row[1]), int(row[2]), int(row[3]))
                    count += 1
            print(f'{count} {"records were" if count > 1 else "record was"} inserted into {no_ext_file}.s3db')


if __name__ == '__main__':
    main()
