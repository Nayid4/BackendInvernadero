from mediatr import Mediator
from application.controles.queries.consultar_control.dto import ControlRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository

@Mediator.handler
class ControlHandler:
    def handle(self, request: ControlRequestDTO):
        crisp = CRISP.get(request.planta)
        if crisp is None:
            return {
                "error": f"Tipo de planta desconocido: {request.planta}"
            }
        fuzzy = FuzzyActuatorsControl(crisp)
        if (crisp['temp_range'][0] <= request.temperatura <= crisp['temp_range'][1] and
            crisp['hum_aire_range'][0] <= request.humedad_aire <= crisp['hum_aire_range'][1] and
            crisp['hum_suelo_range'][0] <= request.humedad_suelo <= crisp['hum_suelo_range'][1]):
            return {
                'rociador': 'off',
                'ventilador': 'off',
                'luminosidad': 'off',
                'recomendacion': 'Ideal: mantener actuadores apagados.'
            }
        return fuzzy.decidir(request.temperatura, request.humedad_aire, request.humedad_suelo)
