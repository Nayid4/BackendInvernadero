from mediatr import Mediator
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class DeletePlantaHandler:
    def handle(self, request):
        repo = PlantaRepository()
        repo.eliminar_planta(request.id)
        return {"success": True}
