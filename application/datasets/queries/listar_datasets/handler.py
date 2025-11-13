from mediatr import Mediator

from application.datasets.queries.listar_datasets.dto import ListCsvDatasetDTO
from infrastructure.repositories.csv_dataset_repository import CsvDatasetRepository


@Mediator.handler
class ListCsvDatasetHandler:
    def handle(self, request: ListCsvDatasetDTO):
        repo = CsvDatasetRepository()
        archivos = repo.listar_archivos()
        return {"archivos": archivos}
