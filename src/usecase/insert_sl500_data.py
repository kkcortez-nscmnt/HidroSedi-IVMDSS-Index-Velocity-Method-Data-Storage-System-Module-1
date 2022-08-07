from src.infra.repositories import DatEntityRepository


class InsertSl500Data:
    """Insere dados .dat no banco de dados"""

    def __init__(self) -> None:
        self.dat_entity_repository = DatEntityRepository

    def _insert_sl500_data_to_data_base(
        self, file_path, initial_time, final_time
    ) -> None:
        self.file_path = file_path
        self.initial_time = initial_time
        self.final_time = final_time
        self.dat_entity_repository.insert_dat(
            self, self.file_path, self.initial_time, self.final_time
        )

        return None
