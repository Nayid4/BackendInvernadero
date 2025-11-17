from mediatr import Mediator
from application.plantas.queries.consultar_optimos_dataset_todas.dto import GetOptimosDatasetTodasDTO
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository

PLANTAS_ESPECIES = ["Tomate", "Lechuga", "Pimenton"]

@Mediator.handler
class GetOptimosDatasetTodasHandler:
    def handle(self, request: GetOptimosDatasetTodasDTO):
        repo = PlantDatasetRepository()
        resultados = {}
        for especie in PLANTAS_ESPECIES:
            try:
                perfil = repo.get_plant_profile(especie)
                optimos = perfil.get("optimos_range")
                universos = perfil.get("universe_of_discourse")
                if optimos and universos:
                    resultados[especie] = {
                        "optimos": optimos,
                        "universe_of_discourse": universos
                    }
                else:
                    resultados[especie] = {
                        "error": "Sin óptimos o universos en dataset"
                    }
            except Exception as e:
                resultados[especie] = {
                    "error": str(e)
                }
        return resultados