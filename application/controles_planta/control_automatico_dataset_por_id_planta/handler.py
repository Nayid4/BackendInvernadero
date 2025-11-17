from mediatr import Mediator
from application.controles_planta.control_automatico_dataset_por_id_planta.dto import ControlAutomaticoDatasetByIdRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl
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

def normalize_range(r):
    if isinstance(r, dict):
        return tuple(sorted([float(r['valMin']), float(r['valMax'])]))
    elif isinstance(r, (list, tuple)) and len(r) == 2:
        return tuple(sorted([float(r[0]), float(r[1])]))
    else:
        raise ValueError(f"Rango no soportado: {repr(r)}")

@Mediator.handler
class ControlAutomaticoDatasetByIdHandler:
    def handle(self, request: ControlAutomaticoDatasetByIdRequestDTO):
        try:
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
            # 3. Obtener valores óptimos registrados desde Firestore (no usar CRISP nunca)
            opt_repo = OptimosPlantaRepository()
            valores = opt_repo.obtener_optimos_por_id(request.idPlanta)
            if not valores:
                return {"error": "No existen parámetros óptimos en el sistema para esta planta (verifica en el sistema de administración)."}
            optimos = {
                    "temp_range": normalize_range(valores["temp_range"]),
                    "hum_suelo_range": normalize_range(valores["hum_suelo_range"]),
                    "hum_aire_range": normalize_range(valores["hum_aire_range"]),
                    "luz_range": normalize_range(valores["luz_range"])
                }
            # 4. Obtener universe_of_discourse del dataset
            universes = {
                "temp_range": profile["universe_of_discourse"]["temp_range"],
                "hum_suelo_range": profile["universe_of_discourse"]["hum_suelo_range"],
                "hum_aire_range": profile["universe_of_discourse"]["hum_aire_range"],
                "luz_range": profile["universe_of_discourse"]["luminosidad_range"]
            }
            # 5. Evaluar dataset completo con lógica difusa ajustada
            fuzzy = FuzzyActuatorsControl(optimos, universes)
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
                'valores_optimos_usados': optimos,
                'universe_of_discourse_usados': universes,
                "total_registros": len(report),
                "coincidencias": sum(all(x["coincidencia"].values()) for x in report),
                "detalle": report
            }
        except Exception as e:
            return {"error": str(e)}
