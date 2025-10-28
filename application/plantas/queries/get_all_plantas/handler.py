from mediatr import Mediator
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class GetAllPlantasHandler:
    def handle(self, request):
        repo = PlantaRepository()
        return repo.obtener_todas_las_plantas()
