from mediatr import Mediator

from application.datasets.queries.download_dataset.dto import DownloadCsvDatasetDTO
from infrastructure.repositories.csv_dataset_repository import CsvDatasetRepository


@Mediator.handler
class DownloadCsvDatasetHandler:
    def handle(self, request: DownloadCsvDatasetDTO):
        repo = CsvDatasetRepository()
        path = repo.descargar_archivo(request.filename)
        return path