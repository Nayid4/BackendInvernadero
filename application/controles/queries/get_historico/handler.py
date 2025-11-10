from mediatr import Mediator
from application.controles.queries.get_historico.dto import GetHistoricoDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository

@Mediator.handler
class GetHistoricoHandler:
    def handle(self, request: GetHistoricoDTO):
        repo = DatosAmbienteRepository()
        historico = repo.get_historico_completo()
        return historico if historico else []
