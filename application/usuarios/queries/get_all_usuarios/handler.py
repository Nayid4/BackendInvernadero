from mediatr import Mediator
from application.usuarios.queries.get_all_usuarios.dto import GetAllUsuariosDTO
from infrastructure.repositories.usuario_repository import UsuarioRepository

@Mediator.handler
class GetAllUsuariosHandler:
    def handle(self, request: GetAllUsuariosDTO):
        repo = UsuarioRepository()
        usuarios = repo.obtener_todos_los_usuarios()
        return usuarios
