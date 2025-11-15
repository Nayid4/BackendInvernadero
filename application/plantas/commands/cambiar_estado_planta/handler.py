from mediatr import Mediator
from application.plantas.commands.cambiar_estado_planta.dto import CambiarEstadoPlantaDTO
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class CambiarEstadoPlantaHandler:
    def handle(self, request: CambiarEstadoPlantaDTO):
        repo = PlantaRepository()
        planta = repo.obtener_planta_por_id(request.id)
        if not planta:
            raise Exception("Planta no encontrada.")
        if request.estado not in ["Activo", "Desactivo"]:
            raise Exception("El estado debe ser 'Activo' o 'Desactivo'.")
        if request.estado == "Activo":
            otra = repo.obtener_planta_activa()
            if otra and otra.id != planta.id:
                otra.estado = "Desactivo"
                repo.actualizar_planta(otra)
        planta.estado = request.estado
        repo.actualizar_planta(planta)
        return {"id": planta.id, "nuevo_estado": planta.estado}