from mediatr import Mediator
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class GetAllUsuariosHandler:
    def handle(self, request):
        repo = UsuarioRepository()
        usuarios = repo.obtener_todos_los_usuarios()
        return usuarios
