from mediatr import Mediator
from application.controles_planta.control_automatico_dataset_por_id_planta.dto import ControlAutomaticoDatasetByIdRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
from infrastructure.repositories.planta_repository import PlantaRepository

PLANTAS_ESPECIES = ["Tomate", "Lechuga", "Pimenton"]

def obtener_especie_desde_nombre(nombre: str):
    nombre_lower = nombre.lower()
    for especie in PLANTAS_ESPECIES:
        if especie.lower() in nombre_lower:
            return especie
    return None

@Mediator.handler
class ControlAutomaticoDatasetByIdHandler:
    def handle(self, request: ControlAutomaticoDatasetByIdRequestDTO):
        # 1. Buscar la planta y determinar especie
        planta_repo = PlantaRepository()
        planta = planta_repo.obtener_planta_por_id(request.idPlanta)
        if not planta:
            return {"error": "Planta no encontrada para el id indicado."}
        especie = obtener_especie_desde_nombre(planta.nombre)
        if not especie:
            return {"error": "La especie detectada no es válida ('Tomate', 'Lechuga', 'Pimenton')."}
        # 2. Dataset de la especie
        profile_repo = PlantDatasetRepository()
        try:
            profile = profile_repo.get_plant_profile(especie)
        except Exception as e:
            return {"error": f"No se pudo cargar el dataset: {str(e)}"}
        # 3. Obtener valores óptimos registrados o CRISP
        opt_repo = OptimosPlantaRepository()
        valores = opt_repo.obtener_optimos_por_id(request.idPlanta)
        if valores:
            crisp = {
                "temp_range": (valores["temp_range"]["valMin"], valores["temp_range"]["valMax"]),
                "hum_suelo_range": (valores["hum_suelo_range"]["valMin"], valores["hum_suelo_range"]["valMax"]),
                "hum_aire_range": (valores["hum_aire_range"]["valMin"], valores["hum_aire_range"]["valMax"]),
                "luz_range": (valores["luz_range"]["valMin"], valores["luz_range"]["valMax"])
            }
        else:
            crisp = CRISP.get(especie)
        if not crisp:
            return {"error": "No existen parámetros óptimos para esta planta/especie."}
        # 4. Evaluar dataset
        fuzzy = FuzzyActuatorsControl(crisp)
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
            "idPlanta": request.idPlanta,
            "especie": especie,
            'valores_optimos_usados': crisp,
            "total_registros": len(report),
            "coincidencias": sum(all(x["coincidencia"].values()) for x in report),
            "detalle": report
        }
