from mediatr import Mediator
from application.plantas.commands.delete_planta.dto import DeletePlantaDTO
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class DeletePlantaHandler:
    def handle(self, request: DeletePlantaDTO):
        repo = PlantaRepository()
        repo.eliminar_planta(request.id)
        return {"success": True}
