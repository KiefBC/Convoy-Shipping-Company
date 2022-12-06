import csv
import re
import database
import conversion


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
            convoy = conversion.Convoy(filename)
            # cv_db.initialize_database()
            if re.match(".*\.(xlsx)$", filename):
                # If the file is an Excel file, convert it to csv
                # This will also clean it
                convoy.convert_xlsx(filename)
            print('THIS IS OUR CSV FILE: ', filename)
            if re.match(".*\.(csv)$", filename):
                convoy.clean_csv(filename)
                cleaned_csv = f'{convoy.convoy_filename[:-4]}[CHECKED].csv'
            else:
                cleaned_csv = f'{convoy.convoy_filename[:-4]}[CHECKED].csv'
                # cleaned_csv = filename
            # else:
            #     cleaned_csv = f'{convoy.convoy_filename[:-4]}[CHECKED].csv'
            # print(f'This is our Cleaned CSV File: {cleaned_csv}')
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
