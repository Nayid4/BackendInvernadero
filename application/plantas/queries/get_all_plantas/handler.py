from mediatr import Mediator
from application.plantas.queries.get_all_plantas.dto import GetAllPlantasDTO
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class GetAllPlantasHandler:
    def handle(self, request: GetAllPlantasDTO):
        repo = PlantaRepository()
        return repo.obtener_todas_las_plantas()
