from mediatr import Mediator
from application.plantas.queries.consultar_planta_activa.dto import ConsultarPlantaActivaDTO
from infrastructure.repositories.planta_repository import PlantaRepository
from flask_problem_details import ProblemDetails, ProblemDetailsError

@Mediator.handler
class ConsultarPlantaActivaHandler:
    def handle(self, request: ConsultarPlantaActivaDTO):
        repo = PlantaRepository()
        planta = repo.obtener_planta_activa()
        if not planta:
            raise ProblemDetailsError(
                ProblemDetails(
                    status=404,
                    title="No hay planta en estado activo",
                    detail="Actualmente no existe ninguna planta activa para monitoreo. Por favor, active una planta desde la administración."
                )
            )
        return planta.to_dict()