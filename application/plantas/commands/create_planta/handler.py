from mediatr import Mediator
from domain.planta import Planta
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class CreatePlantaHandler:
    def handle(self, request):
        planta = Planta(
            id=None,
            nombre=request.nombre,
            especie=request.especie,
            fecha_siembra=request.fecha_siembra,
            ubicacion=request.ubicacion,
            usuario_id=request.usuario_id
        )
        repo = PlantaRepository()
        repo.guardar_planta(planta)
        return {"success": True}
