from mediatr import Mediator

from application.controles_planta.consultar_ultimo_historico_por_id_planta.dto import GetUltimoHistoricoByPlantaIdRequestDTO
from infrastructure.repositories.datos_ambiente_repository import DatosAmbienteRepository
from infrastructure.repositories.planta_repository import PlantaRepository

PLANTAS_ESPECIES = ["tomate", "lechuga", "pimenton"]

def obtener_especie_desde_nombre(nombre: str):
    nombre_lower = nombre.lower()
    for especie in PLANTAS_ESPECIES:
        if especie in nombre_lower:
            return especie
    return None

@Mediator.handler
class GetUltimoHistoricoByPlantaIdHandler:
    def handle(self, request: GetUltimoHistoricoByPlantaIdRequestDTO):
        planta_repo = PlantaRepository()
        planta = planta_repo.obtener_planta_por_id(request.idPlanta)
        if not planta:
            return {"error": "Planta no encontrada para el id indicado."}
        especie = obtener_especie_desde_nombre(planta.nombre)
        if not especie:
            return {"error": "La especie detectada no es válida ('Tomate', 'Lechuga', 'Pimenton')."}
        ambiente_repo = DatosAmbienteRepository()
        historico = ambiente_repo.get_historico_completo()
        filtrado = [h for h in historico if especie in h.planta.lower()]
        if not filtrado:
            return {"error": "No se encontraron registros históricos para la especie."}
        ultimo = sorted(filtrado, key=lambda d: d.fecha)[-1]
        return {
            "id": ultimo.id,
            "fecha": ultimo.fecha,
            "planta": ultimo.planta,
            "temperatura": ultimo.temperatura,
            "humedad_aire": ultimo.humedad_aire,
            "humedad_suelo": ultimo.humedad_suelo
        }
