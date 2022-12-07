import csv
import re
import database
import conversion


def main() -> None:
    """
    Main function
    :return: None
    """
    try:
        filename = input('Input file name\n')
        if not re.match(".*\.(csv|xlsx)", filename):
            print('Make sure you only use .xlsx or .csv extension files\n')
    except FileNotFoundError as e:
        print(f'\nERROR! {e}\n')
    else:
        # Removing the extension from the filename
        no_ext_file = filename[:-5] if filename.endswith('.xlsx') else filename[:-4]
        no_ext_file = re.sub("\[CHECKED\]", "", no_ext_file)
        if re.match(".*\[CHECKED\].csv$", no_ext_file):
            no_ext_file = no_ext_file[:-9]
        cv_db = database.Database(no_ext_file)
        # Establishing connection to the Class
        convoy = conversion.Convoy(filename)
        # Check if the file is a csv file
        if re.match(".*\.(csv)$", filename):
            # Does the file have the [CHECKED] tag?
            if re.match(".*\[CHECKED\].csv$", filename):
                pass
            else:
                convoy.clean_csv(filename)
                cleaned_csv = f'{convoy.convoy_filename[:-4]}[CHECKED].csv'
        # If the file is an Excel file, convert it to csv
        if re.match(".*\.(xlsx)$", filename):
            convoy.convert_xlsx(filename)
            filename = convoy.convoy_filename
        count = 0
        # Insert the data into the database
        with open(f'{no_ext_file}[CHECKED].csv', 'r') as csv_file:
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
