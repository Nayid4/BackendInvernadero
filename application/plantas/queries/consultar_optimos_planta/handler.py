from mediatr import Mediator

from application.plantas.queries.consultar_optimos_planta.dto import GetOptimosPlantaDTO
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository


@Mediator.handler
class GetOptimosPlantaHandler:
    def handle(self, request: GetOptimosPlantaDTO):
        repo = OptimosPlantaRepository()
        datos = repo.obtener_optimos_por_id(request.idPlanta)
        if not datos:
            raise Exception("No existen valores óptimos para la planta indicada.")
        return datos