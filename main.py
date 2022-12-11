import database
import operations
import re


def main() -> None:
    """
    Main function
    :return: None
    """
    try:
        # Ask the user for the filename
        filename = input('Input file name\n')
        if not re.match(".*\.(csv|xlsx|s3db|json|xml)", filename):
            print('Make sure you only use .xlsx, .csv, .s3db, .json, or .xml extension files\n')
    except FileNotFoundError as e:
        print(f'\nERROR! {e}\n')
    else:
        # Removing the extension from the filename xlsx, csv, s3db, json, xml
        # We will use this to create the database name and pass it to the Database class
        pattern = re.compile(r'\.csv$|\[CHECKED\].csv$|\.xlsx$|\.s3db$|\.json$|\.xml$')
        non_extension = pattern.sub('', filename)
        # Initialize our Classes and Database
        db = database.Database(non_extension)
        oper = operations.Convoy(non_extension)
        # Check if the file is a csv file
        if re.match(".*\.(csv)$", filename):
            # Does the file have the [CHECKED] tag?
            if re.match(".*\[CHECKED\].csv$", filename):
                db.add_csv_to_db(filename)
                oper.convert_sqlite_to_json(non_extension)
                oper.convert_to_xml(non_extension)
            else:
                oper.clean_csv(non_extension)
                db.add_csv_to_db(non_extension)
                oper.convert_sqlite_to_json(non_extension)
                oper.convert_to_xml(non_extension)
        # Check if the file is an Excel file
        if re.match(".*\.(xlsx)$", filename):
            oper.convert_xlsx_to_csv(non_extension)
            oper.clean_csv(non_extension)
            db.add_csv_to_db(non_extension)
            oper.convert_sqlite_to_json(non_extension)
            oper.convert_to_xml(non_extension)
        # Check if the file is a SQLite3 database
        if re.match(".*\.(s3db)$", filename):
            oper.convert_sqlite_to_json(non_extension)
            oper.convert_to_xml(non_extension)


if __name__ == '__main__':
    main()
