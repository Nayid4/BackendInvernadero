from mediatr import Mediator
from application.plantas.queries.get_planta_by_id.dto import GetPlantaByIdDTO
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class GetPlantaByIdHandler:
    def handle(self, request: GetPlantaByIdDTO):
        repo = PlantaRepository()
        return repo.obtener_planta_por_id(request.id)
