from abc import ABC, abstractmethod
from domain.usuario import Usuario

class IUsuarioRepository(ABC):
    @abstractmethod
    def guardar_usuario(self, usuario: Usuario):
        pass

    @abstractmethod
    def obtener_usuario_por_correo(self, correo: str):
        pass

    @abstractmethod
    def eliminar_usuario(self, correo: str):
        pass

    @abstractmethod
    def obtener_todos_los_usuarios(self):
        pass
