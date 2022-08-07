from src.infra.repositories import MatEntityRepository


class InsertM9Data:
    """UseCase para registro de dados na DataBase"""

    def __init__(self) -> None:
        self.mat_entity_repository = MatEntityRepository
        self.data_trv = None

    def _insert_m9_data_to_data_base(
        self,
        file_path,
    ) -> None:
        """
        Executa o registo de dados de arquivos .mat
        :param = filepath: String com o path do arquivo .dat

        :return - None
        """
        self.file_path = file_path
        self.mat_entity_repository.insert_mat(
            self,
            self.file_path,
        )
