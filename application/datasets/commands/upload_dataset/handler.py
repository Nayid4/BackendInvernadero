from mediatr import Mediator

from application.datasets.commands.upload_dataset.dto import UploadCsvDatasetDTO
from infrastructure.repositories.csv_dataset_repository import CsvDatasetRepository


@Mediator.handler
class UploadCsvDatasetHandler:
    def handle(self, request: UploadCsvDatasetDTO):
        repo = CsvDatasetRepository()
        nombre = repo.agregar_archivo(request.file_storage)
        return {"success": True, "archivo": nombre}