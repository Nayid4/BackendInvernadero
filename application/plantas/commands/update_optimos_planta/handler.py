from mediatr import Mediator
from application.plantas.commands.update_optimos_planta.dto import UpdateOptimosPlantaDTO
from domain.optimos_planta import OptimosPlanta
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository


@Mediator.handler
class UpdateOptimosPlantaHandler:
    def handle(self, request: UpdateOptimosPlantaDTO):
        repo = OptimosPlantaRepository()
        optimos = OptimosPlanta(
            idPlanta=request.idPlanta,
            temp_range=request.temp_range,
            hum_suelo_range=request.hum_suelo_range,
            hum_aire_range=request.hum_aire_range,
            luz_range=request.luz_range
        )
        repo.actualizar_optimos(optimos)
        return {"success": True}