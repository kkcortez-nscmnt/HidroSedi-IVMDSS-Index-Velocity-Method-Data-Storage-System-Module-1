import logging
import sqlite3


class DBConnectionHandler:
    """
    Conexão com a base de dados SQLite3
    """

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self):
        logging.info("Calling __enter__")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        logging.info("Calling __exit__")
        self.connection.commit()
        self.connection.close()
