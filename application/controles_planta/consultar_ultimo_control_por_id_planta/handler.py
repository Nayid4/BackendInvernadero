from mediatr import Mediator
from application.controles_planta.consultar_ultimo_control_por_id_planta.dto import GetUltimoControlByPlantaIdDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
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
class GetUltimoControlByPlantaIdHandler:
    def handle(self, request: GetUltimoControlByPlantaIdDTO):
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
        # 3. Consultar valores óptimos, usar CRISP si no hay
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
            "valores_optimos_usados": crisp
        }
