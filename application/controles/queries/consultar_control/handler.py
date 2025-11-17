from mediatr import Mediator
from application.controles.queries.consultar_control.dto import ControlRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository

@Mediator.handler
class ControlHandler:
    def handle(self, request: ControlRequestDTO):
        planta_nombre = request.planta.capitalize()  # Uniformar formato

        dataset_repo = PlantDatasetRepository()
        try:
            perfil = dataset_repo.get_plant_profile(planta_nombre)
        except Exception as e:
            return {"error": f"No se pudo cargar los datos para la planta: {str(e)}"}

        optimos = perfil.get("optimos_range")
        universes = perfil.get("universe_of_discourse")

        if not optimos or not universes:
            return {"error": "No existen parámetros óptimos o universos de discurso para esta planta en el dataset."}

        fuzzy = FuzzyActuatorsControl(optimos, universes)

        if (optimos['temp_range'][0] <= request.temperatura <= optimos['temp_range'][1] and
            optimos['hum_aire_range'][0] <= request.humedad_aire <= optimos['hum_aire_range'][1] and
            optimos['hum_suelo_range'][0] <= request.humedad_suelo <= optimos['hum_suelo_range'][1]):
            return {
                'rociador': 'off',
                'ventilador': 'off',
                'luminosidad': 'off',
                'recomendacion': 'Ideal: mantener actuadores apagados.',
                'valores_optimos_usados': optimos,
                'universe_of_discourse_usados': universes
            }

        resultado = fuzzy.decidir(request.temperatura, request.humedad_aire, request.humedad_suelo)
        resultado['valores_optimos_usados'] = optimos
        resultado['universe_of_discourse_usados'] = universes
        return resultado
