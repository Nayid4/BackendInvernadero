from mediatr import Mediator

from application.control_circuito.quieries.consultar_modo_por_id_planta.dto import GetCircuitControlDTO
from infrastructure.repositories.circuit_control_repository import CircuitControlRepository
from infrastructure.repositories.planta_repository import PlantaRepository


@Mediator.handler
class GetCircuitControlHandler:
    def handle(self, request: GetCircuitControlDTO):
        planta_repo = PlantaRepository()
        planta = planta_repo.obtener_planta_por_id(request.idPlanta)
        if not planta:
            return {"error": "Planta no encontrada para el id indicado."}
        repo = CircuitControlRepository()
        result = repo.get_control_mode(request.idPlanta)
        return result or {"error": "No hay configuración para esta planta."}