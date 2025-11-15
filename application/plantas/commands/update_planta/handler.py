from mediatr import Mediator
from application.plantas.commands.update_planta.dto import UpdatePlantaDTO
from infrastructure.repositories.planta_repository import PlantaRepository

PLANTAS_PERMITIDAS = ["Tomate", "Lechuga", "Pimenton"]

def nombre_valido(nombre):
    return any(planta in nombre for planta in PLANTAS_PERMITIDAS)

@Mediator.handler
class UpdatePlantaHandler:
    def handle(self, request: UpdatePlantaDTO):
        repo = PlantaRepository()
        planta = repo.obtener_planta_por_id(request.id)
        if not planta:
            raise Exception("Planta no encontrada")
        if request.nombre:
            if not nombre_valido(request.nombre):
                raise Exception("El nombre de la planta debe incluir 'Tomate', 'Lechuga' o 'Pimenton'")
            planta.nombre = request.nombre
        if request.fecha_siembra:
            planta.fecha_siembra = request.fecha_siembra
        if hasattr(request, "estado") and request.estado is not None:
            if request.estado not in ["Activo", "Desactivo"]:
                raise Exception("El estado solo puede ser 'Activo' o 'Desactivo'.")
            if request.estado == "Activo":
                otra = repo.obtener_planta_activa()
                if otra and otra.id != planta.id:
                    raise Exception("Ya hay una planta activa, primero desactívela.")
                planta.estado = "Activo"
            else:
                planta.estado = "Desactivo"
        repo.actualizar_planta(planta)
        return {"success": True}
