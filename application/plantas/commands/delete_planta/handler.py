from mediatr import Mediator
from application.plantas.commands.delete_planta.dto import DeletePlantaDTO
from infrastructure.repositories.planta_repository import PlantaRepository
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
from infrastructure.repositories.circuit_control_repository import CircuitControlRepository

@Mediator.handler
class DeletePlantaHandler:
    def handle(self, request: DeletePlantaDTO):
        repo = PlantaRepository()
        repo_optimos = OptimosPlantaRepository()
        repo_circuit = CircuitControlRepository()
        # Borra planta principal
        repo.eliminar_planta(request.id)
        # Borra valores óptimos si existen
        try:
            repo_optimos.eliminar_optimos(request.id)
        except Exception:
            pass  # Ignora si no existían
        # Borra modo de circuito si existe
        try:
            repo_circuit.eliminar_control_mode(request.id)
        except Exception:
            pass  # Ignora si no existía
        return {"success": True}
