from mediatr import Mediator
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class GetPlantaByIdHandler:
    def handle(self, request):
        repo = PlantaRepository()
        return repo.obtener_planta_por_id(request.id)
