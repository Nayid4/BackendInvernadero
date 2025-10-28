from mediatr import Mediator
from application.usuarios.queries.get_usuario_by_id.dto import GetUsuarioByIdDTO
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
@Mediator.handler
class GetUsuarioByIdHandler:
    def handle(self, request: GetUsuarioByIdDTO):
        repo = UsuarioRepository()
        usuario = repo.obtener_usuario_por_id(request.id)
        return usuario  # Instancia de Usuario o None

