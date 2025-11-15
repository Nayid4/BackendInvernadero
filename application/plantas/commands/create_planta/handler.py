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
        # Si se pide crear activa, asegurar sólo una activa a la vez
        repo = PlantaRepository()
        estado = getattr(request, "estado", "Desactivo")
        if estado not in ["Activo", "Desactivo"]:
            raise Exception("El estado solo puede ser 'Activo' o 'Desactivo'.")
        if estado == "Activo" and repo.obtener_planta_activa():
            raise Exception("Solo puede haber una planta activa para monitoreo.")
        planta = Planta(
            id=None,
            nombre=request.nombre,
            fecha_siembra=request.fecha_siembra,
            estado=estado,
        )
        repo.guardar_planta(planta)
        circuit_repo = CircuitControlRepository()
        circuit_repo.set_control_mode(planta.id, "automatico")
        return {"success": True, "idPlanta": planta.id}

