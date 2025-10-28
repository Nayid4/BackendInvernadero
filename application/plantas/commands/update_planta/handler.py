from mediatr import Mediator
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class UpdatePlantaHandler:
    def handle(self, request):
        repo = PlantaRepository()
        planta = repo.obtener_planta_por_id(request.id)
        if not planta:
            raise Exception("Planta no encontrada")
        if request.nombre: planta.nombre = request.nombre
        if request.especie: planta.especie = request.especie
        if request.fecha_siembra: planta.fecha_siembra = request.fecha_siembra
        if request.ubicacion: planta.ubicacion = request.ubicacion
        if request.usuario_id: planta.usuario_id = request.usuario_id
        repo.guardar_planta(planta)
        return {"success": True}
