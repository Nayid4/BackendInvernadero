from mediatr import Mediator
from application.usuarios.commands.delete_usuario.dto import DeleteUsuarioDTO
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class DeleteUsuarioHandler:
    def handle(self, request: DeleteUsuarioDTO):
        repo = UsuarioRepository()
        repo.eliminar_usuario(request.id)
        return {"success": True}
