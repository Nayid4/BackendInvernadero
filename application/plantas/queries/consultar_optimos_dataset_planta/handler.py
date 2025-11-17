from mediatr import Mediator
from application.plantas.queries.consultar_optimos_dataset_planta.dto import GetOptimosDatasetPlantaDTO
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository

@Mediator.handler
class GetOptimosDatasetPlantaHandler:
    def handle(self, request: GetOptimosDatasetPlantaDTO):
        repo = PlantDatasetRepository()
        try:
            perfil = repo.get_plant_profile(request.planta.capitalize())
        except Exception as e:
            raise Exception(f"No se pudieron calcular óptimos para {request.planta}: {str(e)}")
        optimos = perfil.get("optimos_range")
        universos = perfil.get("universe_of_discourse")
        if not optimos or not universos:
            raise Exception(f"No existen valores óptimos o universos de discurso en el dataset para: {request.planta}")
        return {"optimos": optimos, "universe_of_discourse": universos}