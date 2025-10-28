from mediatr import Mediator
from application.usuarios.queries.get_usuario_by_correo.dto import GetUsuarioByCorreoDTO
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class GetUsuarioByCorreoHandler:
    def handle(self, request: GetUsuarioByCorreoDTO):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_correo(request.correo)
        return usuario  # Instancia de Usuario o None
