import csv
import sqlite3
from operations import Convoy


class Database:

    def __init__(self, filename: str) -> None:
        self.non_extension = filename
        self.db = f'{filename}.s3db'
        self.conn = sqlite3.connect(f'{filename}.s3db')
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Initialize the database
        :return:
        """
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS convoy (
                vehicle_id INTEGER PRIMARY KEY,
                engine_capacity INTEGER NOT NULL,
                fuel_consumption INTEGER NOT NULL,
                maximum_load INTEGER NOT NULL,
                score INTEGER NOT NULL
            )""")
        self.conn.commit()

    def add_csv_to_db(self, filename: str) -> None:
        """
        Add a vehicle to the database
        :param filename:
        :return:
        """
        c = Convoy(self.non_extension)
        if '[CHECKED]' in filename:
            csv_filename = filename
            db_filename = f'{filename[:-13]}.s3db'
        else:
            csv_filename = f'{filename}[CHECKED].csv'
            db_filename = f'{filename}.s3db'
        counter = 0
        # Select the CSV file
        with open(csv_filename, 'r') as csv_file:
            # Read the CSV file
            file_reader = csv.reader(csv_file, delimiter=',', lineterminator='\n')
            # Loop through the rows
            next(file_reader)
            for row in file_reader:
                counter += 1
                the_score = c.the_score(int(row[1]), int(row[2]), int(row[3]))
                # If the row is not the header
                if row[0] != 'vehicle_id':
                    # Insert the row into the database
                    self.cursor.execute(f"""INSERT or REPLACE INTO convoy VALUES (
                        {row[0]},
                        {row[1]},
                        {row[2]},
                        {row[3]},
                        {the_score}
                    )""")
                    self.conn.commit()
            # Announce how many rows have been added
            print(f'{counter} {"records were" if counter > 1 else "record was"} inserted into {db_filename}')


def main() -> None:
    pass


if __name__ == '__main__':
    main()
