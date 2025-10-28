from abc import ABC, abstractmethod
from domain.planta import Planta

class IPlantaRepository(ABC):
    @abstractmethod
    def guardar_planta(self, planta: Planta):
        pass

    @abstractmethod
    def obtener_planta_por_id(self, planta_id: str):
        pass

    @abstractmethod
    def eliminar_planta(self, planta_id: str):
        pass

    @abstractmethod
    def obtener_todas_las_plantas(self):
        pass
