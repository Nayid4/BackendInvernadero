from mediatr import Mediator
from infrastructure.firebase.firebase_repository import FirebaseUsuarioRepository

@Mediator.handler
class DeleteUsuarioHandler:
    def handle(self, request):
        repo = FirebaseUsuarioRepository()
        repo.eliminar_usuario(request.correo)
        return {"success": True}
