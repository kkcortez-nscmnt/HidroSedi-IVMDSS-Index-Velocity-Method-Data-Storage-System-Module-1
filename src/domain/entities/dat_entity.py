from src.infra.config import DBConnectionHandler


class DatEntity:
    """
    Entidade de Relacionamento Dat_table
    """

    def create_dat_table(self):
        """
        Cria table dat_table em DataBase.db
        :param - None
        :return - None
        """
        with DBConnectionHandler(file_name="DataBase.DB") as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS dat_table (
                    cod INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_time TEXT(10) NOT NULL,
                    velocity_x NUMERIC(10,3) NOT NULL,
                    level NUMERIC(10,3) NOT NULL
                    );
                    """
            )
