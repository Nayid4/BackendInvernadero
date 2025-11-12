from mediatr import Mediator
from application.controles.queries.consultar_historico_por_planta.dto import GetHistoricoPorPlantaDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository


@Mediator.handler
class GetHistoricoPorPlantaHandler:
    def handle(self, request: GetHistoricoPorPlantaDTO):
        repo = DatosAmbienteRepository()
        historico = repo.get_historico_completo()
        if request.planta:
            filtrado = [h for h in historico if h.planta.lower() == request.planta.lower()]
            return filtrado
        return historico
