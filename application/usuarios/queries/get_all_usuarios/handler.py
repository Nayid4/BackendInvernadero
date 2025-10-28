from mediatr import Mediator
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository

@Mediator.handler
class GetAllUsuariosHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        return repo.obtener_todos_los_usuarios()
