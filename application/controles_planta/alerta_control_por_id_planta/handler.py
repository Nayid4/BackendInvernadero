from mediatr import Mediator
from application.controles_planta.alerta_control_por_id_planta.dto import AlertaControlRequestDTO
from infrastructure.repositories.planta_repository import PlantaRepository
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from infrastructure.repositories.optimos_planta_repository import OptimosPlantaRepository
from domain.fuzzy_actuator_control import FuzzyActuatorsControl, CRISP

@Mediator.handler
class AlertaControlHandler:
    def handle(self, request: AlertaControlRequestDTO):
        

        PLANTAS_ESPECIES = ["Tomate", "Lechuga", "Pimenton"]

        def obtener_especie_desde_nombre(nombre: str):
            nombre_lower = nombre.lower()
            for especie in PLANTAS_ESPECIES:
                if especie.lower() in nombre_lower:
                    return especie
            return None

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
        # 4. Pasar por lógica difusa y construir mensaje de alerta
        fuzzy = FuzzyActuatorsControl(crisp)
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
            "valores_optimos_usados": crisp
        }
