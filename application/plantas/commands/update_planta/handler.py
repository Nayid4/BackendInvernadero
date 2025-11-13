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
        repo.actualizar_planta(planta)
        return {"success": True}