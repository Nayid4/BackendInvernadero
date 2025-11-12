
from application.controles.queries.control_automatico_dataset.dto import ControlAutomaticoDatasetRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from mediatr import Mediator

@Mediator.handler
class ControlAutomaticoDatasetHandler:
    def handle(self, request: ControlAutomaticoDatasetRequestDTO):
        profile_repo = PlantDatasetRepository()
        profile = profile_repo.get_plant_profile(request.planta)
        crisp = CRISP.get(request.planta)
        if crisp is None:
            return {
                "error": f"Tipo de planta desconocido: {request.planta}"
            }
        fuzzy = FuzzyActuatorsControl(crisp) # Ya no necesitas el profile aquí
        report = []
        for registro in profile["datos"]:
            entrada = {
                "temperatura": registro["temperatura"],
                "humedad_aire": registro["humedad_aire"],
                "humedad_suelo": registro["humedad_suelo"],
            }
            salida_predicha = fuzzy.decidir(**entrada)
            salida_esperada = {
                "ventilador": registro["ventilador"],
                "rociador": registro["rociador"],
                "luminosidad": registro["luminosidad"]
            }
            comparativo = {
                "entrada": entrada,
                "esperado": salida_esperada,
                "predicho": salida_predicha,
                "coincidencia": {k: salida_esperada[k] == salida_predicha[k] for k in salida_esperada}
            }
            report.append(comparativo)
        return {
            "planta": request.planta,
            "total_registros": len(report),
            "coincidencias": sum(all(x["coincidencia"].values()) for x in report),
            "detalle": report
        }
