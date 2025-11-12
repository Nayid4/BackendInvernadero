from mediatr import Mediator
from application.controles.queries.consultar_ultimo_control.dto import GetUltimoControlRequestDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP
from application.controles.queries.consultar_control.dto import ControlRequestDTO

@Mediator.handler
class GetUltimoControlHandler:
    def handle(self, request: GetUltimoControlRequestDTO):
        repo = DatosAmbienteRepository()
        ultimo = repo.get_ultimo_registro()
        if ultimo is None or not ultimo.planta:
            return {"error": "No existe un registro histórico válido."}
        crisp = CRISP.get(ultimo.planta)
        if crisp is None:
            return {"error": f"Tipo de planta desconocido: {ultimo.planta}"}
        fuzzy = FuzzyActuatorsControl(crisp)
        result = fuzzy.decidir(ultimo.temperatura, ultimo.humedad_aire, ultimo.humedad_suelo)
        return {
            "fecha": ultimo.fecha,
            "planta": ultimo.planta,
            "entrada": {
                "temperatura": ultimo.temperatura,
                "humedad_aire": ultimo.humedad_aire,
                "humedad_suelo": ultimo.humedad_suelo
            },
            "accion_predicha": result
        }
