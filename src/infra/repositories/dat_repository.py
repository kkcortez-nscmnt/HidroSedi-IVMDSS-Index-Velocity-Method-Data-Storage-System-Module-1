from pandas import DataFrame, read_csv, to_datetime
from src.domain.models import DatEntityModel
from src.infra.config import DBConnectionHandler

CONVERTE_DBA_PARA_MCA = 1.092


class DatEntityRepository(DataFrame):
    """
    Implementação do repositorio da entidade DatEntity
    """

    def insert_dat(
        self, file_path: str, initial_time: str, final_time: str
    ) -> DatEntityModel:
        """
        Insere dados na tabela dat_table
        :param - file_path: String com o path do arquivo .dat
               - initial_time: Hora inicial da medida de vazão
               - final_time: Hora final da medidad de vazão
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:

            dat_df = read_csv(file_path, sep="\s+")
            dat_df = dat_df.loc[
                :,
                [
                    "Year",
                    "Month",
                    "Day",
                    "Hour",
                    "Minute",
                    "Second",
                    "VelocityX",
                    "Pressure",
                ],
            ]
            dat_df["Date"] = to_datetime(dat_df.loc[:, "Year":"Second"])
            dat_df = dat_df[(dat_df.Date >= initial_time) & (dat_df.Date <= final_time)]
            date_time = str(dat_df.iat[0, 8])
            velocity_x = round(float(dat_df.iat[0, 6]), 3)
            level = round((float(dat_df.iat[0, 7]) * CONVERTE_DBA_PARA_MCA), 3)

            cursor.execute(
                """ INSERT INTO dat_table (date_time, velocity_x, level) VALUES (?, ?, ?)""",
                (date_time, velocity_x, level),
            )
            dat_model = DatEntityModel(date_time, velocity_x, level)
            return dat_model

    def delete_data_from_dat_table(self) -> None:
        """
        Deleta os dados da dat_table
        :param - None
        :return - None
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            cursor.execute("""Delete from dat_table""")

    def select_velocity_x_from_dat_table(self):
        """
        Seleciona os dados da coluna velocity_x da dat_table.
        :param - None
        return - lista com dados velocity_x
        """
        query_data = None

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            velocity_x_data = cursor.execute("""SELECT velocity_x FROM dat_table""")
            query_data = velocity_x_data
            velocity_x_list = [velocity_x[0] for velocity_x in query_data]
            return velocity_x_list

    def select_level_from_dat_table(self):
        """
        Seleciona os dados da coluna level da dat_table.
        :param - None
        return - lista com dados de level
        """
        query_data = None

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            level_data = cursor.execute("""SELECT level FROM dat_table""")
            query_data = level_data
            level_list = [level[0] for level in query_data]
            return level_list
