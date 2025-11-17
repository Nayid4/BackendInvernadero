from mediatr import Mediator
from application.controles_planta.alerta_control_por_id_planta.dto import AlertaControlRequestDTO
from infrastructure.repositories.plant_profile_repository import PlantDatasetRepository
from infrastructure.repositories.planta_repository import PlantaRepository
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
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
class AlertaControlHandler:
    def handle(self, request: AlertaControlRequestDTO):
        try:
            # 1. Buscar la planta por id
            planta_repo = PlantaRepository()
            planta = planta_repo.obtener_planta_por_id(request.idPlanta)
            if not planta:
                return {"estado": "error", "mensaje": "Planta no encontrada."}
            especie = obtener_especie_desde_nombre(planta.nombre)
            if not especie:
                return {"estado": "error", "mensaje": "La especie detectada no es válida ('Tomate', 'Lechuga', 'Pimenton')."}
            # 2. Buscar el último registro ambiental de la planta/especie
            ambiente_repo = DatosAmbienteRepository()
            historico = ambiente_repo.get_historico_completo()
            historico_filtrado = [h for h in historico if especie.lower() in h.planta.lower()]
            if not historico_filtrado:
                return {"estado": "error", "mensaje": "No hay histórico ambiental para esta especie."}
            ultimo = sorted(historico_filtrado, key=lambda d: d.fecha)[-1]
            # 3. Consultar valores óptimos desde Firestore (no usar CRISP)
            opt_repo = OptimosPlantaRepository()
            valores = opt_repo.obtener_optimos_por_id(request.idPlanta)
            if not valores:
                return {"estado": "error", "mensaje": "No existen parámetros óptimos en el sistema para esta planta, configúrelos en la administración."}
            optimos = {
                        "temp_range": normalize_range(valores["temp_range"]),
                        "hum_suelo_range": normalize_range(valores["hum_suelo_range"]),
                        "hum_aire_range": normalize_range(valores["hum_aire_range"]),
                        "luz_range": normalize_range(valores["luz_range"])
                    }
            # 4. Consultar universe_of_discourse en el dataset real
            dataset_repo = PlantDatasetRepository()
            try:
                perfil = dataset_repo.get_plant_profile(especie)
            except Exception as e:
                return {"estado": "error", "mensaje": f"No se pudo cargar universe_of_discourse para la planta: {str(e)}"}
            universes = {
                "temp_range": perfil["universe_of_discourse"]["temp_range"],
                "hum_suelo_range": perfil["universe_of_discourse"]["hum_suelo_range"],
                "hum_aire_range": perfil["universe_of_discourse"]["hum_aire_range"],
                "luz_range": perfil["universe_of_discourse"]["luminosidad_range"]
            }
            # 5. Pasar por lógica difusa y construir mensaje de alerta
            fuzzy = FuzzyActuatorsControl(optimos, universes)
            decision = fuzzy.decidir(ultimo.temperatura, ultimo.humedad_aire, ultimo.humedad_suelo)
            # Mensajes por cada actuador:
            mensajes = []
            if decision['ventilador'] == 0:
                mensajes.append("Temperatura dentro del rango óptimo, mantener el ventilador apagado.")
            else:
                mensajes.append(f"Alerta: temperatura fuera de rango óptimo, se recomienda encender el ventilador al nivel {decision['ventilador']}.")
            if decision['luminosidad'] == 0:
                mensajes.append("Humedad del aire óptima, mantener sistema de luz apagado.")
            else:
                mensajes.append(f"Alerta: humedad del aire fuera de rango, encender la luminosidad al nivel {decision['luminosidad']}.")
            if decision['rociador'] == 0:
                mensajes.append("Humedad del suelo óptima, mantener el rociador apagado.")
            else:
                mensajes.append(f"Alerta: humedad del suelo fuera de rango óptimo, activar rociador durante {decision['rociador']} segundos.")
            return {
                "estado": "ok",
                "fecha": ultimo.fecha,
                "planta": planta.nombre,
                "entrada": {
                    "temperatura": ultimo.temperatura,
                    "humedad_aire": ultimo.humedad_aire,
                    "humedad_suelo": ultimo.humedad_suelo
                },
                "decision": decision,
                "mensajes_recomendacion": mensajes,
                "valores_optimos_usados": optimos,
                "universe_of_discourse_usados": universes
            }
        except Exception as e:
            return {"estado": "error", "mensaje": str(e)}
