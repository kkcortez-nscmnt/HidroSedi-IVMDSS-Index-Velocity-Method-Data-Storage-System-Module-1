from scipy.io import loadmat
from src.domain.models import MatEntityModel
from src.infra.config import DBConnectionHandler


class MatEntityRepository:
    """
    Implementação do repositorio da entidade MatEntity
    """

    def insert_mat(self, file_path: str) -> MatEntityModel:
        """
        Insere dados na entidade de arquivos MAT
        :param - filepath: String com o path do arquivo .mat
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            mat_df = loadmat(file_path)
            flow_rate = mat_df["Summary"]["Total_Q"]
            flow_rate = flow_rate[0][0][-1][0]
            area = mat_df["Summary"]["Area"]
            area = area[0][0][0][0]
            mean_velocity = flow_rate / area

            # arredondamentos de casas decimais
            rounded_flow_rate = round(flow_rate, 3)
            rounded_area = round(area, 3)
            rounded_mean_velocity = round(mean_velocity, 3)

            cursor.execute(
                """INSERT INTO mat_table ( flow_rate, area, mean_velocity) VALUES (?, ?, ?)""",
                (rounded_flow_rate, rounded_area, rounded_mean_velocity),
            )

            mat_model = MatEntityModel(
                rounded_flow_rate, rounded_area, rounded_mean_velocity
            )

            return mat_model

    def delete_data_from_mat_table(self) -> None:
        """
        Deleta os dados da mat_table
        :param - None
        :return - None
        """

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            cursor.execute("""Delete from mat_table""")

    def select_area_from_mat_table(self):
        """
        Seleciona os dados da coluna area da mat_table.
        :param - None
        return - area data
        """
        query_data = None

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            area_data = cursor.execute("""SELECT area FROM mat_table""")
            query_data = area_data
            area_list = [area[0] for area in query_data]
            print(type(area_list))
            return area_list

    def select_flow_rate_from_mat_table(self):
        """
        Seleciona os dados da coluna flow_rate da mat_table.
        :param - None
        return - area data
        """
        query_data = None

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            flow_rate_data = cursor.execute("""SELECT flow_rate FROM mat_table""")
            query_data = flow_rate_data
            flow_rate_list = [flow_rate[0] for flow_rate in query_data]
            print(type(flow_rate_list))
            return flow_rate_list

    def select_mean_velocity_from_mat_table(self):
        """
        Seleciona os dados da coluna mean_velocity da mat_table.
        :param - None
        return - mean data
        """
        query_data = None

        with DBConnectionHandler(file_name="DataBase.db") as cursor:
            mean_velocity_data = cursor.execute("""SELECT flow_rate FROM mat_table""")
            query_data = mean_velocity_data
            mean_velocity_list = [mean_velocity[0] for mean_velocity in query_data]
            print(type(mean_velocity_list))
            return mean_velocity_list
