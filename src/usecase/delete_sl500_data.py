from src.infra.repositories import DatEntityRepository


class DeleteSL500Data:
    """UseCase para deletar dados na DataBase"""

    def __init__(self) -> None:
        self.dat_entity_repository = DatEntityRepository

    def _delete_SL500_data_to_data_base(
        self,
    ) -> None:
        """
        Deleta o registro de dados de arquivos .dat
        :return - None
        """
        self.dat_entity_repository.delete_data_from_dat_table(self)
        return None
