from mediatr import Mediator
from application.plantas.commands.create_optimos_planta.dto import CreateOptimosPlantaDTO
from domain.optimos_planta import OptimosPlanta
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository

@Mediator.handler
class CreateOptimosPlantaHandler:
    def handle(self, request: CreateOptimosPlantaDTO):
        repo = OptimosPlantaRepository()
        if repo.ya_existen_optimos(request.idPlanta):
            raise Exception("Ya existen valores óptimos registrados para esta planta. Use 'PUT' para actualizar.")
        optimos = OptimosPlanta(
            idPlanta=request.idPlanta,
            temp_range=request.temp_range,
            hum_suelo_range=request.hum_suelo_range,
            hum_aire_range=request.hum_aire_range,
            luz_range=request.luz_range
        )
        repo.guardar_optimos(optimos)
        return {"success": True}