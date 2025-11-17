from mediatr import Mediator
from application.controles.queries.consultar_ultimo_control.dto import GetUltimoControlRequestDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from domain.fuzzy_actuator_control import FuzzyActuatorsControl

@Mediator.handler
class GetUltimoControlHandler:
    def handle(self, request: GetUltimoControlRequestDTO):
        repo = DatosAmbienteRepository()
        ultimo = repo.get_ultimo_registro()
        if ultimo is None or not ultimo.planta:
            return {"error": "No existe un registro histórico válido."}
        
        # Usar nombre para extraer rangos y óptimos del dataset
        planta_nombre = ultimo.planta.capitalize()
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
        result = fuzzy.decidir(ultimo.temperatura, ultimo.humedad_aire, ultimo.humedad_suelo)
        return {
            "fecha": ultimo.fecha,
            "planta": ultimo.planta,
            "entrada": {
                "temperatura": ultimo.temperatura,
                "humedad_aire": ultimo.humedad_aire,
                "humedad_suelo": ultimo.humedad_suelo
            },
            "accion_predicha": result,
            "valores_optimos_usados": optimos,
            "universe_of_discourse_usados": universes
        }
