# The Repository
import sqlite3

from DAO import DAO
import DTO


class Repository:
    def __init__(self, args):
        self._conn = sqlite3.connect(args[4])
        self.hats = DAO(DTO.Hat, self._conn)
        self.suppliers = DAO(DTO.Supplier, self._conn)
        self.orders = DAO(DTO.Order, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
            id  INT PRIMARY KEY,
            topping TEXT NOT NULL,
            supplier INT REFERENCES suppliers(id),
            quantity INT NOT NULL
        );

        CREATE TABLE suppliers (
            id INT PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE orders (
            id INT PRIMARY KEY,
            location TEXT NOT NULL,
            hat INT REFERENCES hats(id)
        );
    """)


