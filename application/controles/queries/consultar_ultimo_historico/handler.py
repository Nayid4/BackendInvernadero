from mediatr import Mediator
from application.controles.queries.consultar_ultimo_historico.dto import GetUltimoHistoricoRequestDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository

@Mediator.handler
class GetUltimoHistoricoHandler:
    def handle(self, request: GetUltimoHistoricoRequestDTO):
        repo = DatosAmbienteRepository()
        ultimo = repo.get_ultimo_registro()
        if ultimo is None:
            return {"error": "No existe un registro histórico válido."}
        return {
            "id": ultimo.id,
            "fecha": ultimo.fecha,
            "planta": ultimo.planta,
            "temperatura": ultimo.temperatura,
            "humedad_aire": ultimo.humedad_aire,
            "humedad_suelo": ultimo.humedad_suelo
        }
