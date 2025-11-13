from mediatr import Mediator

from application.datasets.commands.delete_dataset.dto import DeleteCsvDatasetDTO
from infrastructure.repositories.csv_dataset_repository import CsvDatasetRepository


@Mediator.handler
class DeleteCsvDatasetHandler:
    def handle(self, request: DeleteCsvDatasetDTO):
        repo = CsvDatasetRepository()
        repo.eliminar_archivo(request.filename)
        return {"success": True}