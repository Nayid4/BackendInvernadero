from mediatr import Mediator
from application.controles_planta.consultar_ultimo_control_por_id_planta.dto import GetUltimoControlByPlantaIdDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from infrastructure.repositories.planta_repository import PlantaRepository
from domain.fuzzy_actuator_control import FuzzyActuatorsControl

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
class GetUltimoControlByPlantaIdHandler:
    def handle(self, request: GetUltimoControlByPlantaIdDTO):
        try:
            # 1. Buscar la planta por id
            planta_repo = PlantaRepository()
            planta = planta_repo.obtener_planta_por_id(request.idPlanta)
            if not planta:
                return {"error": "Planta no encontrada para el id indicado."}
            especie = obtener_especie_desde_nombre(planta.nombre)
            if not especie:
                return {"error": "La especie detectada no es válida ('Tomate', 'Lechuga', 'Pimenton')."}
            # 2. Filtrar el histórico por especie y buscar el último registro
            ambiente_repo = DatosAmbienteRepository()
            historico = ambiente_repo.get_historico_completo()
            historico_filtrado = [h for h in historico if especie.lower() in h.planta.lower()]
            if not historico_filtrado:
                return {"error": "No existe histórico para la especie indicada."}
            ultimo_registro = sorted(historico_filtrado, key=lambda d: d.fecha)[-1]
            # 3. Consultar valores óptimos desde Firestore (no usar CRISP)
            opt_repo = OptimosPlantaRepository()
            valores = opt_repo.obtener_optimos_por_id(request.idPlanta)
            if not valores:
                return {"error": "No existen parámetros óptimos para esta planta (verifica en el sistema de administración)."}
            optimos = {
                "temp_range": normalize_range(valores["temp_range"]),
                "hum_suelo_range": normalize_range(valores["hum_suelo_range"]),
                "hum_aire_range": normalize_range(valores["hum_aire_range"]),
                "luz_range": normalize_range(valores["luz_range"])
            }

            # 4. Consultar universe_of_discourse real desde dataset
            dataset_repo = PlantDatasetRepository()
            try:
                perfil = dataset_repo.get_plant_profile(especie)
            except Exception as e:
                return {"error": f"No se pudo cargar universe_of_discourse para la planta: {str(e)}"}
            universes = {
                "temp_range": perfil["universe_of_discourse"]["temp_range"],
                "hum_suelo_range": perfil["universe_of_discourse"]["hum_suelo_range"],
                "hum_aire_range": perfil["universe_of_discourse"]["hum_aire_range"],
                "luz_range": perfil["universe_of_discourse"]["luminosidad_range"]
            }
            # 5. Lógica difusa con ambos parámetros
            fuzzy = FuzzyActuatorsControl(optimos, universes)
            resultado = fuzzy.decidir(
                ultimo_registro.temperatura,
                ultimo_registro.humedad_aire,
                ultimo_registro.humedad_suelo
            )
            return {
                    "fecha": ultimo_registro.fecha,
                    "planta": ultimo_registro.planta,
                    "entrada": {
                        "temperatura": ultimo_registro.temperatura,
                        "humedad_aire": ultimo_registro.humedad_aire,
                        "humedad_suelo": ultimo_registro.humedad_suelo
                    },
                    "accion_predicha": resultado,
                    "valores_optimos_usados": optimos,
                    "universe_of_discourse_usados": universes
                }
        except Exception as e:
            return {"error": str(e)}
