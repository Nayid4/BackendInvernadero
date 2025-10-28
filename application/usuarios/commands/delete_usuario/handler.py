from mediatr import Mediator
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class DeleteUsuarioHandler:
    def handle(self, request):
        repo = UsuarioRepository()
        repo.eliminar_usuario(request.id)
        return {"success": True}
