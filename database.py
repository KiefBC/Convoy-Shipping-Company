import sqlite3
from os.path import exists


class Database:

    def __init__(self, filename: str):
        self.name = filename
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
                maximum_load INTEGER NOT NULL
            )""")
        self.conn.commit()

    def add_vehicle(self, vehicle_id: int, engine_capacity: int, fuel_consumption: int, maximum_load: int) -> None:
        """
        Add a vehicle to the database
        :param vehicle_id:
        :param engine_capacity:
        :param fuel_consumption:
        :param maximum_load:
        :return:
        """

        self.cursor.execute("INSERT or REPLACE INTO convoy VALUES (?,?,?,?)",
                            (vehicle_id, engine_capacity, fuel_consumption, maximum_load))
        self.conn.commit()


def main():
    database = Database()


if __name__ == '__main__':
    main()
