# from src.domain.dat_models import DatEntityModel
from src.infra.config import DBConnectionHandler

from ..dat_repository import DatEntityRepository

# from src.infra.entities import DatEntity


dat_repository = DatEntityRepository()
db_connection_handler = DBConnectionHandler(file_name="DataBase.db")


# file_path = "test_files/2018_03_29_HS-SL-SG-02.dat"
# initial_time = "2018-04-17 11:00:02"
# final_time = "2018-04-17 11:19:35"


file_path = "test_files/2018_03_13_HS-SL-SG-02.dat"
# initial_time = "2018-03-13 18:11:19"
# final_time = "2018-03-13 18:21:55"

initial_time = "2018-03-21 11:14:04"
final_time = "2018-03-21 11:28:12"

# initial_time = '2018-03-21 14:50:39'
# final_time = '2018-03-21 15:02:49'

# initial_time = "2018-04-04 15:42:41"
# final_time = "2018-04-04 15:55:33"

# initial_time = '2018-04-11 11:30:18'
# final_time = '2018-04-11 11:44:08'

# initial_time = '2018-04-11 17:06:01'
# final_time = '2018-04-11 17:17:18'


def test_insert_dat():
    """Deve inserir dados do tipo Dat"""

    # inserindo dados
    new_dat_data = dat_repository.insert_dat(file_path, initial_time, final_time)

    # SQL query

    with DBConnectionHandler("DataBase.db") as cursor:
        query_dat_data = cursor.execute(
            "SELECT cod, date_time, velocity_x, level FROM dat_table;"
        ).fetchone()

        print(new_dat_data)
        print(query_dat_data)

        assert new_dat_data[0] == query_dat_data[1]
        assert new_dat_data[1] == query_dat_data[2]
        assert new_dat_data[2] == query_dat_data[3]


def test_select_velocity_from_dat():
    """Deve retornar os dados selecionados"""

    selected_data = dat_repository.select_velocity_x_from_dat_table()
    print(selected_data)


def test_level_from_dat():
    """
    Deve retornar os dados selecionados
    """
    selected_data = dat_repository.select_level_from_dat_table()
    print(selected_data)


# def test_delete_from_dat():
#     """
#     Deve deletar dados da data base
#     """
#     dat_repository.delete_data_from_dat_table_table()
#     print("Dados deletados")
