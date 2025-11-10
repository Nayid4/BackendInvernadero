from mediatr import Mediator
from application.controles.queries.consultar_control.dto import ControlRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository

@Mediator.handler
class ControlHandler:
    def handle(self, request: ControlRequestDTO):
        profile_repo = PlantDatasetRepository()
        profile = profile_repo.get_plant_profile(request.planta)
        fuzzy = FuzzyActuatorsControl(profile)
        if (profile['temp_range'][0] <= request.temperatura <= profile['temp_range'][1] and
            profile['hum_aire_range'][0] <= request.humedad_aire <= profile['hum_aire_range'][1] and
            profile['hum_suelo_range'][0] <= request.humedad_suelo <= profile['hum_suelo_range'][1]):
            return {
                'bomba': 'off',
                'ventilador': 'off',
                'luz': 'off',
                'recomendacion': 'Ideal: mantener actuadores apagados.',
                'centroide': profile['centroide']
            }
        return fuzzy.decidir(request.temperatura, request.humedad_aire, request.humedad_suelo)

