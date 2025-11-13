from mediatr import Mediator
from application.plantas.commands.create_planta.dto import CreatePlantaDTO
from domain.planta import Planta
from infrastructure.repositories.circuit_control_repository import CircuitControlRepository
from infrastructure.repositories.planta_repository import PlantaRepository

PLANTAS_PERMITIDAS = ["Tomate", "Lechuga", "Pimenton"]

def nombre_valido(nombre):
    return any(planta in nombre for planta in PLANTAS_PERMITIDAS)

@Mediator.handler
class CreatePlantaHandler:
    def handle(self, request: CreatePlantaDTO):
        if not nombre_valido(request.nombre):
            raise Exception("El nombre de la planta debe incluir 'Tomate', 'Lechuga' o 'Pimenton'")
        planta = Planta(
            id=None,
            nombre=request.nombre,
            fecha_siembra=request.fecha_siembra,
        )
        repo = PlantaRepository()
        repo.guardar_planta(planta)
        # planta.id ya contiene el id generado
        circuit_repo = CircuitControlRepository()
        circuit_repo.set_control_mode(planta.id, "automatico")
        return {"success": True, "idPlanta": planta.id}
