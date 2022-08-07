# from src.domain.dat_models import DatEntityModel
from src.infra.config import DBConnectionHandler

from ..mat_repository import MatEntityRepository

mat_repository = MatEntityRepository()
db_connection_handler = DBConnectionHandler(file_name="DataBase.db")


def test_insert_mat():
    """Deve inserir dados do tipo Dat"""
    file_path = "test_files/20180313181930.mat"

    # inserindo dados
    new_mat_data = mat_repository.insert_mat(file_path)

    # SQL query
    with DBConnectionHandler("DataBase.db") as cursor:
        query_mat_data = cursor.execute(
            "SELECT cod, flow_rate, area, mean_velocity FROM mat_table;"
        ).fetchone()

        print(new_mat_data)
        print(query_mat_data)

        assert new_mat_data[0] == query_mat_data[1]
        assert new_mat_data[1] == query_mat_data[2]
        assert new_mat_data[2] == query_mat_data[3]


def test_select_flow_rate_mat():
    """Deve retornar os dados selecionados"""

    selected_data = mat_repository.select_flow_rate_from_mat_table()
    print(selected_data)


def test_select_mean_velocity_from_dat():
    """
    Deve retornar os dados selecionados
    """
    selected_data = mat_repository.select_mean_velocity_from_mat_table()
    print(selected_data)


# def test_delete_from_mat():
#     """
#     Deve deletar dados da data base
#     """
#     mat_repository.delete_data_from_mat_table_table()
#     print("Dados deletados")
