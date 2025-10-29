from mediatr import Mediator
from application.abanico.queries.consultar_abanico.dto import ConsultarAbanicoDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from domain.control_abanico_simpful import ControlAbanicoSimpful

@Mediator.handler
class ConsultarAbanicoHandler:
    def handle(self, request: ConsultarAbanicoDTO):
        repo = DatosAmbienteRepository()
        dato = repo.get_ultimo_registro()
        if not dato:
            return {"fan_on": False}
        modelo = ControlAbanicoSimpful()
        fan_on = modelo.decidir(
            temperatura=dato.temperatura,
            humedad_ambiental=dato.humedad_ambiental,
            humedad_suelo=dato.humedad_suelo
        )
        return {"fan_on": bool(fan_on)}
