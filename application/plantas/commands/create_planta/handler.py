from mediatr import Mediator
from application.plantas.commands.create_planta.dto import CreatePlantaDTO
from domain.planta import Planta
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class CreatePlantaHandler:
    def handle(self, request: CreatePlantaDTO):
        planta = Planta(
            id=None,
            nombre=request.nombre,
            especie=request.especie,
            fecha_siembra=request.fecha_siembra,
            ubicacion=request.ubicacion
        )
        repo = PlantaRepository()
        repo.guardar_planta(planta)
        return {"success": True}
