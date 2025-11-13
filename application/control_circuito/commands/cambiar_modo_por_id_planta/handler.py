from mediatr import Mediator
from application.control_circuito.commands.cambiar_modo_por_id_planta.dto import SetCircuitControlDTO
from infrastructure.repositories.circuit_control_repository import CircuitControlRepository
from infrastructure.repositories.planta_repository import PlantaRepository

@Mediator.handler
class SetCircuitControlHandler:
    def handle(self, request: SetCircuitControlDTO):
        planta_repo = PlantaRepository()
        planta = planta_repo.obtener_planta_por_id(request.idPlanta)
        if not planta:
            return {"error": "Planta no encontrada para el id indicado."}
        repo = CircuitControlRepository()
        repo.set_control_mode(request.idPlanta, request.modo, request.ventilador, request.rociador, request.luminosidad)
        return {"success": True}