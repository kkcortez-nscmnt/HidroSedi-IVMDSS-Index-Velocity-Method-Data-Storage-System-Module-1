from src.infra.repositories import MatEntityRepository


class DeleteM9Data:
    """UseCase para deletar dados na DataBase"""

    def __init__(self) -> None:
        self.mat_entity_repository = MatEntityRepository

    def _delete_m9_data_to_data_base(
        self,
    ) -> None:
        """
        Deleta o registro de dados de arquivos .mat
        :return - None
        """
        self.mat_entity_repository.delete_data_from_mat_table(self)
        return None
