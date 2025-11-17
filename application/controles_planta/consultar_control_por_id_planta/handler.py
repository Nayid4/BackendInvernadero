from mediatr import Mediator
from application.controles_planta.consultar_control_por_id_planta.dto import ControlByIdRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from infrastructure.repositories.planta_repository import PlantaRepository

PLANTAS_ESPECIES = ["Tomate", "Lechuga", "Pimenton"]

def obtener_especie_desde_nombre(nombre: str):
    nombre_lower = nombre.lower()
    for especie in PLANTAS_ESPECIES:
        if especie.lower() in nombre_lower:
            return especie
    return None

def normalize_range_float(r):
    """
    Recibe lista, tupla o dict {'valMin', 'valMax'}, devuelve tupla ordenada (min, max) de float.
    """
    if isinstance(r, (list, tuple)) and len(r) == 2:
        return tuple(sorted([float(r[0]), float(r[1])]))
    elif isinstance(r, dict):
        return tuple(sorted([float(r['valMin']), float(r['valMax'])]))
    else:
        raise ValueError(f"Rango no soportado: {repr(r)}")

def normalize_range_int(r):
    """
    Recibe lista, tupla o dict {'valMin', 'valMax'}, devuelve tupla ordenada (min, max) de int.
    """
    if isinstance(r, (list, tuple)) and len(r) == 2:
        return tuple(sorted([int(round(float(r[0]))), int(round(float(r[1])))]))
    elif isinstance(r, dict):
        return tuple(sorted([int(round(float(r['valMin']))), int(round(float(r['valMax'])))]))
    else:
        raise ValueError(f"Rango no soportado: {repr(r)}")

@Mediator.handler
class ControlByIdHandler:
    def handle(self, request: ControlByIdRequestDTO):
        try:
            # 1. Buscar planta por id
            planta_repo = PlantaRepository()
            planta = planta_repo.obtener_planta_por_id(request.idPlanta)
            if not planta:
                return {"error": "Planta no encontrada para el id indicado."}
            especie = obtener_especie_desde_nombre(planta.nombre)
            if not especie:
                return {"error": "La especie detectada no es válida ('Tomate', 'Lechuga', 'Pimenton')."}
            # 2. Consultar valores óptimos registrados
            opt_repo = OptimosPlantaRepository()
            valores = opt_repo.obtener_optimos_por_id(request.idPlanta)
            if not valores:
                return {"error": "No existen parámetros óptimos para esta planta/especie."}
            try:
                optimos = {
                    "temp_range": normalize_range_float(valores["temp_range"]),
                    "hum_suelo_range": normalize_range_float(valores["hum_suelo_range"]),
                    "hum_aire_range": normalize_range_float(valores["hum_aire_range"]),
                    "luz_range": normalize_range_float(valores["luz_range"])
                }
            except Exception as e:
                return {"error": f"Valores óptimos mal formados en la base de datos: {str(e)}"}
            # 3. Consultar universe_of_discourse real desde el dataset (como ENTEROS)
            dataset_repo = PlantDatasetRepository()
            try:
                perfil = dataset_repo.get_plant_profile(especie)
            except Exception as e:
                return {"error": f"No se pudo cargar universe_of_discourse para la planta: {str(e)}"}
            universes = {
                "temp_range": normalize_range_float(perfil["universe_of_discourse"]["temp_range"]),
                "hum_suelo_range": normalize_range_float(perfil["universe_of_discourse"]["hum_suelo_range"]),
                "hum_aire_range": normalize_range_float(perfil["universe_of_discourse"]["hum_aire_range"]),
                "luz_range": normalize_range_float(perfil["universe_of_discourse"]["luminosidad_range"])
            }

            print(f"Optimos usados: {optimos}")
            print(f"Universos usados: {universes}")

            # 4. Decidir con lógica difusa
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
            result = fuzzy.decidir(request.temperatura, request.humedad_aire, request.humedad_suelo)
            result['valores_optimos_usados'] = optimos
            result['universe_of_discourse_usados'] = universes
            return result
        except Exception as e:
            # Todos los errores inesperados, aunque raros, devuelven error dict para ser 404 en ProblemDetails
            return {"error": str(e)}
