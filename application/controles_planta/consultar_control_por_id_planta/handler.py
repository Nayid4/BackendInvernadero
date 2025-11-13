from mediatr import Mediator
from application.controles.queries.consultar_control.dto import ControlRequestDTO
from application.controles_planta.consultar_control_por_id_planta.dto import ControlByIdRequestDTO
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP
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
class ControlByIdHandler:
    def handle(self, request: ControlByIdRequestDTO):
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
        fuzzy = FuzzyActuatorsControl(crisp)
        if (crisp['temp_range'][0] <= request.temperatura <= crisp['temp_range'][1] and
            crisp['hum_aire_range'][0] <= request.humedad_aire <= crisp['hum_aire_range'][1] and
            crisp['hum_suelo_range'][0] <= request.humedad_suelo <= crisp['hum_suelo_range'][1]):
            return {
                'rociador': 'off',
                'ventilador': 'off',
                'luminosidad': 'off',
                'recomendacion': 'Ideal: mantener actuadores apagados.',
                'valores_optimos_usados': crisp
            }
        result = fuzzy.decidir(request.temperatura, request.humedad_aire, request.humedad_suelo)
        result['valores_optimos_usados'] = crisp
        return result
