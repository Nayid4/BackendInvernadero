from mediatr import Mediator
from application.controles_planta.consultar_historico_por_id_planta.dto import GetHistoricoByPlantaIdDTO
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
class GetHistoricoByPlantaIdHandler:
    def handle(self, request: GetHistoricoByPlantaIdDTO):
        # 1. Buscar la planta por id para obtener el nombre
        planta_repo = PlantaRepository()
        planta = planta_repo.obtener_planta_por_id(request.idPlanta)
        if not planta:
            raise Exception("Planta no encontrada para el id indicado.")
        especie_detectada = obtener_especie_desde_nombre(planta.nombre)
        if not especie_detectada:
            raise Exception("La especie de la planta registrada no es válida: debe contener 'Tomate', 'Lechuga' o 'Pimenton'.")
        # 2. Filtrar el histórico por especie detectada en el campo 'planta'
        ambiente_repo = DatosAmbienteRepository()
        historico = ambiente_repo.get_historico_completo()
        filtrado = [h for h in historico if especie_detectada in h.planta.lower()]
        return filtrado
