from src.infra.config import DBConnectionHandler


class MatEntity:
    """
    Entidade de Relacionamento mat_table
    """

    def create_mat_table(self):
        """
        Cria table mat_table em DataBase.db
        :param - None
        :return - None
        """
        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS mat_table (
                    cod INTEGER PRIMARY KEY AUTOINCREMENT,
                    flow_rate NUMERIC(10,3) NOT NULL,
                    area NUMERIC(10,3) NOT NULL,
                    mean_velocity NUMERIC(10,3) NOT NULL
                    );
                    """
            )
